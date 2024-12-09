"""SQLFluff 嵌套查询检查插件."""

from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_Green_L003(BaseRule):
    """检查SQL嵌套查询的层数.
    
    SELECT 
    d.department_name,
    (SELECT 
        AVG(e2.salary)
        FROM employees e2
        WHERE e2.department_id = d.department_id
        AND e2.salary > (
            SELECT 
                AVG(e3.salary) * 1.5
                FROM employees e3
                WHERE e3.department_id = e2.department_id
                AND e3.manager_id IN (
                    SELECT 
                        e4.employee_id
                        FROM employees e4
                        WHERE e4.department_id = e3.department_id
                        AND e4.hire_date > (
                            SELECT 
                                MIN(e5.hire_date)
                                FROM employees e5
                                WHERE e5.department_id = e4.department_id
                                AND EXTRACT(YEAR FROM e5.hire_date) = 2023
                        )
                )
        )
    ) as high_salary_avg
FROM departments d
WHERE EXISTS (
    SELECT 1 
    FROM employees e1
    WHERE e1.department_id = d.department_id
    AND e1.salary > 50000
);

    规则:
    1. SQL嵌套查询层数不得超过3层
    """

    groups = ("all",)
    targets = {"greenplum"}
    crawl_behaviour = SegmentSeekerCrawler({
        "select_statement",
        "set_expression"
    })

    def _eval(self, context: RuleContext):
        """评估SQL嵌套层数是否符合规范."""
        if not context.segment.is_type("select_statement", "set_expression"):
            return None

        # 获取所有父级select语句
        select_stack = []
        for parent in context.parent_stack:
            if parent.is_type("select_statement", "set_expression"):
                select_stack.append(parent)

        # 当前select也要计入
        nesting_level = len(select_stack) + 1

        # 如果嵌套层数超过3层
        max_nesting = 3
        if nesting_level > max_nesting:
            # 定位到第4个select（从外向内数）
            if len(select_stack) >= max_nesting:
                # 从外向内数第4个select的位置
                anchor_segment = context.segment
            else:
                # 如果当前是第4个或更深层的select
                anchor_segment = context.segment

            return LintResult(
                anchor=anchor_segment,
                description=(
                    f"SQL查询嵌套层数过深。"
                    f"当前嵌套层数: {nesting_level}，"
                    f"最大允许层数: {max_nesting}"
                )
            )

        return None
