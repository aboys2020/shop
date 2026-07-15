"""京东搜索页采集器。"""

import re
import uuid
from datetime import datetime
from typing import List
from urllib.parse import quote

import httpx
from bs4 import BeautifulSoup

from ..models import ProductItem
from .base import BaseScraper


class JDScraper(BaseScraper):
    """京东搜索页解析（真实环境可能受反爬限制）。"""

    platform = "jd"

    def __init__(self, timeout: int = 15) -> None:
        self.timeout = timeout
        self.session = httpx.Client(
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9",
            },
            follow_redirects=True,
            timeout=timeout,
        )

    def search(self, keyword: str, limit: int = 10) -> List[ProductItem]:
        url = f"https://search.jd.com/Search?keyword={quote(keyword)}&enc=utf-8"
        resp = self.session.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        items: List[ProductItem] = []
        for node in soup.select(".gl-item")[:limit]:
            title_node = node.select_one(".p-name a em")
            if not title_node:
                continue
            title = title_node.get_text(strip=True)

            price_text = node.select_one(".p-price i")
            price = self._parse_price(price_text.get_text(strip=True) if price_text else "")

            sales_text = node.select_one(".p-commit a")
            sales = self._parse_sales(sales_text.get_text(strip=True) if sales_text else "0")

            shop_text = node.select_one(".p-shop a")
            shop_name = shop_text.get_text(strip=True) if shop_text else "京东第三方"

            rating = 4.6

            link_node = node.select_one(".p-name a")
            href = link_node.get("href", "") if link_node else ""
            if href and not href.startswith("http"):
                href = "https:" + href

            items.append(
                ProductItem(
                    id=str(uuid.uuid4())[:8],
                    platform=self.platform,
                    keyword=keyword,
                    title=title,
                    price=price,
                    sales=sales,
                    shop_name=shop_name,
                    shop_rating=rating,
                    url=href or url,
                    fetched_at=datetime.now(),
                )
            )

        if not items:
            raise RuntimeError("京东页面未解析到商品，可能触发反爬或页面结构变更")
        return items

    @staticmethod
    def _parse_price(text: str) -> float:
        numbers = re.findall(r"\d+\.?\d*", text.replace(",", ""))
        return float(numbers[0]) if numbers else 0.0

    @staticmethod
    def _parse_sales(text: str) -> int:
        text = text.replace(",", "").replace("+", "")
        match = re.search(r"(\d+\.?\d*)", text)
        if not match:
            return 0
        value = float(match.group(1))
        if "万" in text:
            value *= 10000
        return int(value)
