"""SQLFluff FULL JOIN限制插件，建议使用LEFT JOIN替代FULL JOIN."""

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

# 使用RotatingFileHandler实现日志轮转
from logging.handlers import RotatingFileHandler
log_file = os.path.join(log_dir, "segment_tree.log")

# 创建UTF-8编码的日志处理器，每个日志文件最大10MB，保留3个备份
file_handler = RotatingFileHandler(
    log_file, 
    encoding='utf-8',
    maxBytes=10*1024*1024, 
    backupCount=3
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))

# 配置logger
logger = logging.getLogger('segment_tree')
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

# 添加控制台日志输出
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))
logger.addHandler(console_handler)

class Rule_Green_L039(BaseRule):
    """限制FULL JOIN使用，建议使用LEFT JOIN替代."""

    groups = ("all",)
    targets = {"greenplum"}
    crawl_behaviour = SegmentSeekerCrawler({
        "join_clause",
    })

    def _print_segment_tree(self, segment, level=0):
        """以树形结构打印segment并写入日志."""
        indent = "    " * level
        segment_info = f"{segment.type}"
        if hasattr(segment, 'raw'):
            segment_info += f": {segment.raw}"
        tree_line = f"{indent}├── {segment_info}"

        # 同时输出到控制台和日志文件
        print(tree_line)
        logger.info(tree_line)

        # 打印所有segment，不进行类型过滤
        if hasattr(segment, 'segments'):
            for child in segment.segments:
                self._print_segment_tree(child, level + 1)

    def _eval(self, context: RuleContext):
        # 打印segment树形结构
        # logger.info("\n=== Segment Tree Structure ===")
        # self._print_segment_tree(context.segment)
        # logger.info("============================\n")

        # 检查是否是join_clause
        if context.segment.is_type("join_clause"):
            full_keyword = None
            for seg in context.segment.segments:
                # 先定位FULL关键字
                if seg.raw.upper() == "FULL" and seg.type == 'keyword':
                    full_keyword = seg
                # 当找到JOIN关键字且前一个是FULL时触发规则
                elif seg.raw.upper() == "JOIN" and full_keyword:
                    return LintResult(
                        anchor=full_keyword,
                        description="避免使用FULL JOIN，建议使用LEFT JOIN替代。",
                    )
                # 重置FULL标记（如果中间有其他元素间隔）
                elif seg.type not in ('whitespace', 'newline'):
                    full_keyword = None

        return None

