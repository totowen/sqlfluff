from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler

class Rule_Green_L040(BaseRule):
    """避免使用GROUP BY进行去重，建议使用DISTINCT替代"""
    
    groups = ("all",)
    targets = {"greenplum"}
    crawl_behaviour = SegmentSeekerCrawler({"select_statement"})

    def _eval(self, context: RuleContext):
        if context.segment.is_type("select_statement"):
            has_groupby = False
            has_aggregate = False
            
            # 检查是否存在GROUP BY子句
            for clause in context.segment.get_children("groupby_clause"):
                has_groupby = True
                break
                
            # 检查SELECT是否包含聚合函数
            for expression in context.segment.get_children("select_clause"):
                for func in expression.get_children("function"):
                    if func.raw.lower() in {"count", "sum", "avg", "min", "max"}:
                        has_aggregate = True
                        break
                        
            # 当存在GROUP BY但没有聚合函数时触发规则
            if has_groupby and not has_aggregate:
                return LintResult(
                    anchor=context.segment,
                    description="发现使用GROUP BY进行去重，建议改用DISTINCT关键字"
                )
        return None

