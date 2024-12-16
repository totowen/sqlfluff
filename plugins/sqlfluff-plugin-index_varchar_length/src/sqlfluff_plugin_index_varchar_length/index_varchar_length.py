"""SQLFluff VARCHAR索引长度检查插件."""

import os
import logging
from datetime import datetime
from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


# # 配置日志
# log_dir = "logs"
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)

# log_file = os.path.join(log_dir, f"segment_tree_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# # 创建UTF-8编码的文件处理器
# file_handler = logging.FileHandler(log_file, encoding='utf-8')
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(logging.Formatter('%(message)s'))

# # 配置logger
# logger = logging.getLogger('segment_tree')
# logger.setLevel(logging.INFO)
# logger.addHandler(file_handler)

class Rule_Green_L023(BaseRule):
    """检查VARCHAR类型索引字段的长度.

    规则:
    1. 在GreenPlum中，如果VARCHAR类型字段有索引，建议长度不超过50
    2. VARCHAR长度过长会影响索引效率
    """

    groups = ("all",)
    targets = {"greenplum"}
    crawl_behaviour = SegmentSeekerCrawler({
        "create_table_statement",
        "bracketed",
        "column_reference",
        "data_type",
        "table_constraint"
    })

    # def _print_segment_tree(self, segment, level=0):
    #     """以树形结构打印segment并写入日志."""
    #     indent = "    " * level
    #     segment_info = f"{segment.type}"
    #     if hasattr(segment, 'raw'):
    #         segment_info += f": {segment.raw}"
    #     tree_line = f"{indent}├── {segment_info}"
        
    #     # 同时输出到控制台和日志文件
    #     # print(tree_line)
    #     # logger.info(tree_line)
        
    #     if hasattr(segment, 'segments'):
    #         for child in segment.segments:
    #             self._print_segment_tree(child, level + 1)

    def _eval(self, context: RuleContext):
        """评估VARCHAR索引字段长度."""
        # # 打印segment树形结构
        # logger.info("\n=== Segment Tree Structure ===")
        # self._print_segment_tree(context.segment)
        # logger.info("============================\n")

        # 检查CREATE TABLE语句
        if context.segment.is_type("create_table_statement"):
            # 存储VARCHAR字段信息
            varchar_fields = {}  # {column_name: length}
            lint_results = []  # 存储所有需要提示的结果
            
            # 查找表定义的bracketed
            for seg in context.segment.segments:
                if seg.is_type("bracketed"):
                    current_column = None
                    
                    # 遍历bracketed中的所有segment
                    for child in seg.segments:
                        # 获取列名
                        if child.is_type("column_reference"):
                            current_column = child.raw
                        
                        # 检查数据类型
                        elif child.is_type("data_type") and current_column:
                            if "VARCHAR" in child.raw.upper():
                                try:
                                    length_str = child.raw.split("(")[1].split(")")[0]
                                    length = int(length_str)
                                    if length > 50:
                                        varchar_fields[current_column] = length
                                except (IndexError, ValueError):
                                    continue
                        
                        # 检查表约束中的索引列
                        elif child.is_type("table_constraint"):
                            constraint_columns = []
                            is_index = False
                            
                            # 遍历约束定义
                            for const_seg in child.segments:
                                if const_seg.is_type("keyword"):
                                    if const_seg.raw.upper() in ["PRIMARY KEY", "UNIQUE"]:
                                        is_index = True
                                elif const_seg.is_type("bracketed") and is_index:
                                    # 获取约束中的列名
                                    for col_seg in const_seg.segments:
                                        if col_seg.is_type("column_reference"):
                                            column_name = col_seg.raw
                                            if column_name in varchar_fields:
                                                lint_results.append(
                                                    LintResult(
                                                        anchor=col_seg,
                                                        description=(
                                                            f"列 '{column_name}' 是VARCHAR({varchar_fields[column_name]})类型且有索引，"
                                                            "建议长度不超过50以提高索引效率"
                                                        )
                                                    )
                                                )
            
            return lint_results if lint_results else None
        
        return None
