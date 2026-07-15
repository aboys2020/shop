"""采集器工厂。"""

from typing import Dict, Type

from .base import BaseScraper
from .demo import DemoScraper
from .jd import JDScraper
from .pdd import PDDScraper
from .taobao import TaobaoScraper


class ScraperFactory:
    """根据平台与模式返回对应采集器。"""

    _real: Dict[str, Type[BaseScraper]] = {
        "jd": JDScraper,
        "taobao": TaobaoScraper,
        "pdd": PDDScraper,
    }

    @classmethod
    def get_scraper(cls, platform: str, mode: str = "real") -> BaseScraper:
        platform = platform.lower().strip()
        if platform not in cls._real:
            raise ValueError(f"不支持的平台: {platform}")
        if mode == "demo":
            return DemoScraper(platform=platform)
        return cls._real[platform]()

    @classmethod
    def supported_platforms(cls) -> list[str]:
        return list(cls._real.keys())
