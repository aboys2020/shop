"""统一数据模型。"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any
import hashlib


@dataclass(frozen=True)
class ProductItem:
    """跨平台商品条目。"""

    id: str
    platform: str
    keyword: str
    title: str
    price: float
    sales: int
    shop_name: str
    shop_rating: float
    url: str
    fetched_at: datetime

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["fetched_at"] = self.fetched_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProductItem":
        data = dict(data)
        data["fetched_at"] = datetime.fromisoformat(data["fetched_at"])
        return cls(**data)

    def dedup_key(self) -> str:
        """用于去重的稳定键。"""
        raw = f"{self.platform}|{self.title.strip().lower()}|{self.price}|{self.shop_name.strip().lower()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
