"""演示数据生成器。"""

import random
import uuid
from datetime import datetime
from typing import List

from ..models import ProductItem
from .base import BaseScraper


_PLATFORM_META = {
    "jd": {
        "price_base": 180.0,
        "price_scale": 120.0,
        "sales_base": 500,
        "sales_scale": 5000,
        "rating_base": 4.6,
        "rating_scale": 0.35,
        "shops": ["京东自营", "旗舰数码专营店", "优选生活馆", "品牌官方店", "极速达超市"],
        "suffixes": ["【京东配送】", "【旗舰同款】", "【正品保障】", "【限时特惠】", ""],
    },
    "taobao": {
        "price_base": 140.0,
        "price_scale": 140.0,
        "sales_base": 800,
        "sales_scale": 8000,
        "rating_base": 4.5,
        "rating_scale": 0.4,
        "shops": ["淘好物精选", "潮流数码铺", "天天特价店", "匠心手作坊", "品质优选城"],
        "suffixes": ["【包邮】", "【热销爆款】", "【买一送一】", "【淘宝推荐】", ""],
    },
    "pdd": {
        "price_base": 90.0,
        "price_scale": 90.0,
        "sales_base": 1200,
        "sales_scale": 12000,
        "rating_base": 4.4,
        "rating_scale": 0.45,
        "shops": ["百亿补贴官方", "拼团特惠店", "厂家直销铺", "天天秒杀店", "正品补贴馆"],
        "suffixes": ["【百亿补贴】", "【拼团价】", "【已拼10万+】", "【官方正品】", ""],
    },
}

_URL_TEMPLATES = {
    "jd": "https://search.jd.com/Search?keyword={keyword}&enc=utf-8",
    "taobao": "https://s.taobao.com/search?q={keyword}",
    "pdd": "https://mobile.yangkeduo.com/search_result.html?search_key={keyword}",
}


class DemoScraper(BaseScraper):
    """无需真实请求，生成符合各平台特征的合成数据。"""

    platform = "demo"

    def __init__(self, platform: str = "demo") -> None:
        self.platform = platform

    def search(self, keyword: str, limit: int = 10) -> List[ProductItem]:
        meta = _PLATFORM_META.get(self.platform, _PLATFORM_META["jd"])
        rng = random.Random(f"{self.platform}:{keyword}:{limit}")
        items: List[ProductItem] = []
        titles = [
            f"{keyword} 新款升级版",
            f"{keyword} 官方正品",
            f"{keyword} 性价比之选",
            f"{keyword} 旗舰同款",
            f"{keyword} 轻薄便携款",
            f"{keyword} 家庭装",
            f"{keyword} 专业版",
            f"{keyword} 入门款",
            f"{keyword} 礼盒装",
            f"{keyword} 热销推荐",
        ]
        for i in range(limit):
            title = titles[i % len(titles)] + rng.choice(meta["suffixes"])
            price = round(
                max(9.9, rng.gauss(meta["price_base"], meta["price_scale"])), 2
            )
            sales = int(max(0, rng.gauss(meta["sales_base"], meta["sales_scale"])))
            shop = rng.choice(meta["shops"])
            rating = round(min(5.0, max(3.0, rng.gauss(meta["rating_base"], meta["rating_scale"]))), 2)
            items.append(
                ProductItem(
                    id=str(uuid.uuid4())[:8],
                    platform=self.platform,
                    keyword=keyword,
                    title=title,
                    price=price,
                    sales=sales,
                    shop_name=shop,
                    shop_rating=rating,
                    url=_URL_TEMPLATES.get(self.platform, "").format(keyword=keyword),
                    fetched_at=datetime.now(),
                )
            )
        return items
