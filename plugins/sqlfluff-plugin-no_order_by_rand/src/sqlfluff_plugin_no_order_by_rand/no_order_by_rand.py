"""SQLFluff UPDATE/DELETE LIMIT检查插件."""

import os
import logging
from datetime import datetime
from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


# 配置日志
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"segment_tree_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# 创建UTF-8编码的文件处理器
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(message)s'))

# 配置logger
logger = logging.getLogger('segment_tree')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

class Rule_Green_L035(BaseRule):
    """检查UPDATE和DELETE语句中的LIMIT使用."""

    groups = ("all",)
    targets = {"greenplum"}
    crawl_behaviour = SegmentSeekerCrawler({
        "orderby_clause",
        "expression",
    })

    def _print_segment_tree(self, segment, level=0):
        """以树形结构打印segment并写入日志."""
        indent = "    " * level
        segment_info = f"{segment.type}"
        if hasattr(segment, 'raw'):
            segment_info += f": {segment.raw}"
        tree_line = f"{indent}├── {segment_info}"

        # 同时输出到控制台和日志文件
        # print(tree_line)
        logger.info(tree_line)

        if hasattr(segment, 'segments'):
            for child in segment.segments:
                self._print_segment_tree(child, level + 1)

    def _eval(self, context: RuleContext):
        # 打印segment树形结构
        logger.info("\n=== Segment Tree Structure ===")
        self._print_segment_tree(context.segment)
        logger.info("============================\n")

        # 检查是否是orderby_clause
        if context.segment.is_type("orderby_clause"):
            for seg in context.segment.segments:
                # 检查expression中是否包含RAND()或RANDOM()
                if seg.is_type("expression") and any(
                    func.raw.upper() in ["RAND()", "RANDOM()"] for func in seg.segments
                ):
                    return LintResult(
                        anchor=seg,
                        description="不允许在ORDER BY中使用RAND()或RANDOM()函数，因为这会导致不可预测的排序。",
                    )

        return None

