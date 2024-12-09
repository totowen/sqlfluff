"""SQLFluff LIKE前缀通配符检查插件."""

from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_Green_L022(BaseRule):
    """检查LIKE语句中的前缀通配符.

    规则:
    1. 在GreenPlum中不建议使用前缀模糊查询(LIKE '%xxx')，这会导致全表扫描
    2. 建议使用后缀模糊查询(LIKE 'xxx%')以提高查询性能
    """

    groups = ("all",)
    targets = {"greenplum"}
    crawl_behaviour = SegmentSeekerCrawler({
        # 表相关
        "statement",
        "select_statement",

        # 表达式相关
        "expression",
        "literal",

        # 其他
        "keyword",
    })

    def _eval(self, context: RuleContext):
        """评估LIKE语句."""
        # 打印当前 segment 的类型
        # print(f"当前 segment 类型: {context.segment.type}")

        # 打印所有子 segment 的类型和名称
        # for seg in context.segment.segments:
            # print(f"子 segment 类型: {seg.type}, 名称: {seg.raw if hasattr(seg, 'raw') else '无'}")

        # 检查expression中的literal
        if context.segment.is_type("expression"):
            has_like = False
            for seg in context.segment.segments:
                # 检查是否是LIKE操作符
                if (seg.is_type("keyword") 
                    and seg.raw.upper() == "LIKE"):
                    has_like = True
                    continue
                
                # 如果前面有LIKE，检查literal是否以%开头
                if has_like and seg.is_type(("literal")):
                    value = seg.raw.strip("'\"")
                    if value.startswith("%"):
                        return LintResult(
                            anchor=seg,
                            description="不建议使用前缀模糊查询(LIKE '%xxx')，这会导致全表扫描，影响查询性能。建议使用后缀模糊查询(LIKE 'xxx%')",
                        )
                    has_like = False  # 重置标志
        
        return None
