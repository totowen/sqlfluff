"""SQLFluff 精度类型检查插件."""

from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_Green_L004(BaseRule):
    """检查浮点数类型的使用规范.

    规则:
    1. 存储精确浮点数必须使用DECIMAL替代FLOAT和DOUBLE
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
        
        # 检查是否使用了不推荐的浮点类型
        invalid_types = {"FLOAT", "DOUBLE", "DOUBLE PRECISION", "REAL"}
        if data_type in invalid_types:
            return LintResult(
                anchor=context.segment,
                description=(
                    f"不建议使用 {data_type} 类型存储精确浮点数，"
                    f"建议使用 DECIMAL 类型替代。"
                )
            )

        return None
