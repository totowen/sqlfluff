"""SQLFluff 标识符长度检查插件."""

from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_Green_L002(BaseRule):
    """检查SQL标识符的长度.
    
    规则:
    1. 库名、表名、字段名长度不得超过30个字符
    """

    groups = ("all",)
    config_keywords = ["forbidden_columns"]
    crawl_behaviour = SegmentSeekerCrawler({
        "identifier",
        "column_reference",
        "table_reference",
        "qualified_identifier",
        "schema_reference"
    })
    is_fix_compatible = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.forbidden_columns = [
            col.strip() for col in self.forbidden_columns.split(",")
        ]

    def _eval(self, context: RuleContext):
        """评估标识符长度是否符合规范."""
        if context.segment.is_type("comment", "literal"):
            return None

        # 处理标识符
        if not context.segment.is_type(
            "identifier",
            "table_reference",
            "column_reference",
            "qualified_identifier",
            "schema_reference"
        ):
            return None

        identifier_segment = None
        if context.segment.is_type("identifier"):
            identifier_segment = context.segment
        else:
            for seg in context.segment.segments:
                if seg.is_type("identifier"):
                    identifier_segment = seg
                    break

        if not identifier_segment:
            return None

        raw_identifier = identifier_segment.raw
        if raw_identifier.startswith('"') and raw_identifier.endswith('"'):
            raw_identifier = raw_identifier[1:-1]

        # 检查标识符长度
        max_length = 30
        if len(raw_identifier) > max_length:
            return LintResult(
                anchor=identifier_segment,
                description=(
                    f"标识符 '{raw_identifier}' 超出最大长度限制。"
                    f"当前长度: {len(raw_identifier)}，"
                    f"最大允许长度: {max_length}"
                )
            )

        return None