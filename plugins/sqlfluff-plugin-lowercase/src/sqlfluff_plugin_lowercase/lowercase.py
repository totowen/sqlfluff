"""SQLFluff 标识符命名规范检查插件."""

import re
from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
    LintFix,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_Green_L001(BaseRule):
    """检查SQL标识符的命名规范.

    规则:
    1. 标识符应该使用小写字母
    2. 多个单词之间使用下划线分隔
    3. 特殊字符（除了点号）应该转换为下划线
    """

    groups = ("all",)
    targets = {"greenplum"}
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

    def normalize_identifier(self, name):
        """标准化标识符名称."""
        # 如果已经包含下划线，只进行大小写转换
        if '_' in name:
            return name.lower()

        # 处理特殊字符
        normalized = re.sub(r'[^\w.]', '_', name)
        # 处理驼峰命名
        normalized = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', normalized)
        normalized = re.sub('([a-z0-9])([A-Z])', r'\1_\2', normalized)
        return normalized.lower()

    def create_fixed_segment(self, original_segment, new_raw):
        """创建修复后的段."""
        try:
            return original_segment.__class__(
                raw=new_raw,
                pos_marker=original_segment.pos_marker
            )
        except TypeError:
            fixed = original_segment.copy()
            fixed.raw = new_raw
            return fixed

    def _eval(self, context: RuleContext):
        """评估标识符是否符合命名规范."""
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
            return None

        needs_conversion = (
            any(c.isupper() for c in raw_identifier) or
            any(c for c in raw_identifier if not c.isalnum() and c not in ['_', '.'])
        )

        if not needs_conversion:
            return None

        suggested_name = self.normalize_identifier(raw_identifier)
        if raw_identifier == suggested_name:
            return None

        fixed_segment = self.create_fixed_segment(identifier_segment, suggested_name)

        changes = []
        if any(c.isupper() for c in raw_identifier):
            changes.append("小写")
        if any(c for c in raw_identifier if not c.isalnum() and c not in ['_', '.']):
            changes.append("下划线分隔")

        return LintResult(
            anchor=identifier_segment,
            description=(
                f"标识符 '{raw_identifier}' 需要转换为"
                f"{' 和 '.join(changes)}格式。"
                f"建议修改为: '{suggested_name}'"
            ),
            fixes=[
                LintFix(
                    "replace",
                    identifier_segment,
                    [fixed_segment]
                )
            ]
        )
