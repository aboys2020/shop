"""电商价格采集与对比工具核心模块。"""

from .models import ProductItem
from .processor import process_items, compute_stats
from .scrapers.factory import ScraperFactory

__all__ = ["ProductItem", "process_items", "compute_stats", "ScraperFactory"]
