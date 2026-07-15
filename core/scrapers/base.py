"""采集器抽象基类。"""

from abc import ABC, abstractmethod
from typing import List
from ..models import ProductItem


class BaseScraper(ABC):
    """所有平台采集器的基类。"""

    platform: str = ""

    @abstractmethod
    def search(self, keyword: str, limit: int = 10) -> List[ProductItem]:
        """按关键词搜索并返回商品列表。"""
        raise NotImplementedError
