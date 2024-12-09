"""SQLFluff TEXT和bytea类型检查插件."""

from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_Green_L009(BaseRule):
    """检查TEXT和bytea类型的使用规范.

    规则:
    1. 尽可能不使用TEXT类型，建议使用VARCHAR(n)替代
    2. 尽可能不使用bytea类型，建议使用适当的替代方案
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
        if data_type == "TEXT":
            return LintResult(
                anchor=context.segment,
                description=(
                    f"不建议使用 {data_type} 类型，"
                    f"建议使用 VARCHAR(n) 类型替代，"
                    f"并明确指定长度限制。"
                )
            )
        elif data_type == "BYTEA":
            return LintResult(
                anchor=context.segment,
                description=(
                    f"不建议使用 {data_type} 类型，"
                    f"建议根据实际需求选择以下方案：\n"
                    f"1. 使用文件系统存储文件，数据库只存储路径\n"
                    f"2. 使用对象存储系统（如S3）存储数据\n"
                    f"3. 如果数据量较小，可以使用 VARCHAR 存储 Base64 编码的数据"
                )
            )

        return None
