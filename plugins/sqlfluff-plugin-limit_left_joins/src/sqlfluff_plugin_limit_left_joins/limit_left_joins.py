from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler

class Rule_Green_L041(BaseRule):
    """限制LEFT JOIN使用次数"""
    
    groups = ("all",)
    targets = {"greenplum"}
    config_keywords = ["max_left_joins"]
    crawl_behaviour = SegmentSeekerCrawler({"from_clause"})  # 保持从from_clause开始遍历

    # 新增初始化方法处理配置参数
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置默认值并处理参数类型
        self.max_left_joins = int(getattr(self, 'max_left_joins', 3))
        # 添加参数验证
        if self.max_left_joins < 1:
            raise ValueError("max_left_joins 必须大于等于1")

    def _eval(self, context: RuleContext):
        max_joins = self.max_left_joins  # 从配置获取阈值
        print("max_joins: ",max_joins)
        # 统计所有LEFT JOIN
        join_count = 0

        # 遍历所有join_clause及其子元素
        for join_clause in context.segment.recursive_crawl("join_clause"):
            left_keyword = None
            for seg in join_clause.segments:
                # 检查LEFT关键字
                if seg.raw.upper() == "LEFT" and seg.type == 'keyword':
                    left_keyword = seg
                # 当找到JOIN且前有LEFT时计数
                elif seg.raw.upper() == "JOIN" and left_keyword:
                    join_count += 1
                    left_keyword = None  # 重置状态
                # 遇到非空白字符时重置状态
                elif seg.type not in ('whitespace', 'newline'):
                    left_keyword = None

        if join_count > max_joins:
            return LintResult(
                anchor=context.segment,
                description=f"LEFT JOIN使用次数超过限制（最大允许{max_joins}次），建议优化查询逻辑"
            )
        return None