"""SQLFluff NOT NULL约束检查插件."""

from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_Green_L014(BaseRule):
    """检查字段定义.

    规则:
    1. 在GreenPlum中建议字段定义为NOT NULL，避免使用NULL值
    2. SERIAL类型和PRIMARY KEY字段隐含NOT NULL约束
    """

    groups = ("all",)
    targets = {"greenplum"}
    crawl_behaviour = SegmentSeekerCrawler({
        # 表相关
        "file", 
        "statement",
        "create_table_statement",
        "alter_table_statement",
        "table_definition",
        "table_reference",
        "table_expression",
        
        # 列相关
        "column_definition",
        "column_constraint",
        "column_constraint_segment",
        "column_reference",
        "column_name",
        "column_list",
        
        # 约束相关
        "constraint_definition",
        "constraint_common_segment",
        "table_constraint",
        "constraint",
        "not_null_constraint",
        "null_constraint",
        "check_constraint",
        "unique_constraint",
        "foreign_key_constraint",
        "primary_key_constraint",
        "references_constraint",
        
        # 数据类型相关
        "data_type",
        "data_type_identifier",
        "primitive_type",
        "datetime_type_identifier",
        
        # 表达式相关
        "expression",
        "default_expression",
        "literal",
        
        # 标识符相关
        "identifier",
        "naked_identifier",
        "quoted_identifier",
        
        # 其他
        "comment",
        "whitespace",
        "newline",
        "comma",
        "bracketed",
        "start_bracket",
        "end_bracket",
        "keyword",
    })

    def _eval(self, context: RuleContext):
        """评估字段定义."""
        # # 打印当前 segment 的类型
        # print(f"当前 segment 类型: {context.segment.type}")

        # # 打印所有子 segment 的类型和名称
        # for seg in context.segment.segments:
        #     print(f"子 segment 类型: {seg.type}, 名称: {seg.raw if hasattr(seg, 'raw') else '无'}")
        
        lint_results = []
        
        # 检查创建表语句
        if context.segment.is_type("create_table_statement"):
            # 查找括号内的表定义部分
            bracketed_segment = None
            for seg in context.segment.segments:
                if seg.is_type("bracketed"):
                    bracketed_segment = seg
                    break
            
            if bracketed_segment:
                current_column_segment = None
                has_not_null = False
                is_serial = False
                is_primary_key = False
                column_segments = []
                
                # 遍历括号内的所有子segment
                for seg in bracketed_segment.segments:
                    # 开始新列定义
                    if seg.is_type("column_reference"):
                        # 处理前一个列的检查结果
                        if current_column_segment and not (has_not_null or is_serial or is_primary_key):
                            lint_results.append(
                                LintResult(
                                    anchor=current_column_segment,
                                    description=f"列 '{current_column_segment.raw}' 应该添加 NOT NULL 约束",
                                    fixes=[]
                                )
                            )
                        
                        # 重置状态
                        current_column_segment = seg
                        column_segments = [seg]
                        has_not_null = False
                        is_serial = False
                        is_primary_key = False
                    elif current_column_segment:
                        column_segments.append(seg)
                        
                        # 检查数据类型
                        if seg.is_type("data_type"):
                            if "SERIAL" in seg.raw.upper():
                                is_serial = True
                        
                        # 检查约束
                        elif seg.is_type("column_constraint_segment"):
                            constraint_text = seg.raw.upper()
                            if "NOT NULL" in constraint_text:
                                has_not_null = True
                            if "PRIMARY KEY" in constraint_text:
                                is_primary_key = True
                        
                        # 列定义结束
                        elif seg.is_type("symbol") and seg.raw in [",", ")"]:
                            if not (has_not_null or is_serial or is_primary_key):
                                lint_results.append(
                                    LintResult(
                                        anchor=current_column_segment,
                                        description=f"列 '{current_column_segment.raw}' 应该添加 NOT NULL 约束",
                                        fixes=[]
                                    )
                                )
                            current_column_segment = None
                            column_segments = []
        
        # 检查ALTER TABLE语句
        elif context.segment.is_type("alter_table_statement"):
            for seg in context.segment.segments:
                if seg.is_type("alter_table_action_segment"):
                    # 检查ADD COLUMN操作
                    if "ADD" in seg.raw.upper() and "COLUMN" in seg.raw.upper():
                        # 如果是ADD COLUMN但没有NOT NULL约束
                        if "NOT NULL" not in seg.raw.upper():
                            # 获取列名
                            column_name = None
                            for sub_seg in seg.segments:
                                if sub_seg.is_type("column_reference"):
                                    column_name = sub_seg.raw
                                    break
                            
                            # 检查是否是SERIAL类型或PRIMARY KEY
                            is_serial = "SERIAL" in seg.raw.upper()
                            is_primary_key = "PRIMARY KEY" in seg.raw.upper()
                            
                            if not (is_serial or is_primary_key):
                                lint_results.append(
                                    LintResult(
                                        anchor=seg,
                                        description=f"新增列 '{column_name}' 应该添加 NOT NULL 约束",
                                        fixes=[]
                                    )
                                )
                    
                    # 检查ALTER COLUMN操作
                    elif "ALTER" in seg.raw.upper() and "COLUMN" in seg.raw.upper():
                        # 获取列名
                        column_name = None
                        for sub_seg in seg.segments:
                            if sub_seg.is_type("column_reference"):
                                column_name = sub_seg.raw
                                break
                        
                        # 只有当ALTER COLUMN后面没有任何操作，或者是SET DATA TYPE/SET DEFAULT操作时才提示
                        if column_name:
                            raw_text = seg.raw.upper()
                            if (
                                "SET NOT NULL" not in raw_text 
                                and (
                                    "SET DATA TYPE" in raw_text 
                                    or "SET DEFAULT" in raw_text
                                    or raw_text.strip().endswith(column_name.upper())  # 没有任何操作
                                )
                            ):
                                lint_results.append(
                                    LintResult(
                                        anchor=seg,
                                        description=f"修改列 '{column_name}' 时应该设置 NOT NULL 约束",
                                        fixes=[]
                                    )
                                )

        return lint_results if lint_results else None