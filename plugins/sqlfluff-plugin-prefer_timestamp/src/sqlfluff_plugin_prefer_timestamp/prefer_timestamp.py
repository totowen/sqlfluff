"""SQLFluff 时间类型检查插件."""

from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_Green_L013(BaseRule):
    """检查时间类型的使用规范.

    规则:
    1. 在GreenPlum中建议使用TIMESTAMP类型来存储时间，而不是DATETIME
    """

    groups = ("all",)
    targets = {"greenplum"}
    crawl_behaviour = SegmentSeekerCrawler({
        "data_type",
    })

    def _eval(self, context: RuleContext):
        """评估数据类型是否符合规范."""
        if not context.segment.is_type("data_type"):
            return None

        # 检查是否在DDL语句中
        in_ddl = False
        for parent in context.parent_stack:
            if parent.is_type(
                "create_table_statement",      # CREATE TABLE
                "alter_table_statement",       # ALTER TABLE
                "create_view_statement",       # CREATE VIEW
                "create_materialized_view_statement",  # CREATE MATERIALIZED VIEW
                "alter_view_statement",        # ALTER VIEW
                "create_type_statement",       # CREATE TYPE
                "alter_type_statement"         # ALTER TYPE
            ):
                in_ddl = True
                break

        if not in_ddl:
            return None

        # 获取数据类型名称
        data_type = context.segment.raw.upper()
        
        # 检查是否使用了不推荐的类型
        if data_type == "DATETIME":
            return LintResult(
                anchor=context.segment,
                description=(
                    f"在GreenPlum中不建议使用 {data_type} 类型存储时间，"
                    f"建议使用 TIMESTAMP 类型替代。"
                    f"TIMESTAMP类型提供了更好的时区支持和更高的精度。"
                )
            )

        return None
