"""数据清洗、去重、排序与性价比评分。"""

import math
from typing import Any, Dict, List

from .models import ProductItem


def _clean_title(title: str) -> str:
    return " ".join(title.split())


def process_items(items: List[ProductItem]) -> List[ProductItem]:
    """清洗、去重、按价格升序排序并计算性价比分数。"""
    cleaned: List[ProductItem] = []
    seen: set[str] = set()

    for item in items:
        if item.price <= 0:
            continue
        title = _clean_title(item.title)
        if not title:
            continue
        key = item.dedup_key()
        if key in seen:
            continue
        seen.add(key)

        value_score = _compute_value_score(item.price, item.sales, item.shop_rating)

        cleaned.append(
            ProductItem(
                id=item.id,
                platform=item.platform,
                keyword=item.keyword,
                title=title,
                price=item.price,
                sales=item.sales,
                shop_name=item.shop_name,
                shop_rating=item.shop_rating,
                url=item.url,
                fetched_at=item.fetched_at,
            )
        )

    cleaned.sort(key=lambda x: (x.price, -x.sales))
    return cleaned


def _compute_value_score(price: float, sales: int, rating: float) -> float:
    """性价比分数：评分与销量对数的乘积除以价格。"""
    if price <= 0:
        return 0.0
    return round((rating * math.log(max(sales, 0) + 1)) / price * 1000, 4)


def compute_stats(items: List[ProductItem]) -> Dict[str, Any]:
    """计算统计指标。"""
    if not items:
        return {
            "platform_distribution": {},
            "price_range": {"min": 0.0, "max": 0.0, "avg": 0.0},
            "value_top3": [],
        }

    prices = [item.price for item in items]
    distribution: Dict[str, int] = {}
    for item in items:
        distribution[item.platform] = distribution.get(item.platform, 0) + 1

    sorted_by_value = sorted(
        items,
        key=lambda x: _compute_value_score(x.price, x.sales, x.shop_rating),
        reverse=True,
    )

    return {
        "platform_distribution": distribution,
        "price_range": {
            "min": round(min(prices), 2),
            "max": round(max(prices), 2),
            "avg": round(sum(prices) / len(prices), 2),
        },
        "value_top3": [item.to_dict() for item in sorted_by_value[:3]],
    }
