"""拼多多搜索页采集器。"""

import re
import uuid
from datetime import datetime
from typing import List
from urllib.parse import quote

import httpx
from bs4 import BeautifulSoup

from ..models import ProductItem
from .base import BaseScraper


class PDDScraper(BaseScraper):
    """拼多多搜索页解析（移动端 H5，真实环境可能受反爬限制）。"""

    platform = "pdd"

    def __init__(self, timeout: int = 15) -> None:
        self.timeout = timeout
        self.session = httpx.Client(
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 "
                    "(KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9",
            },
            follow_redirects=True,
            timeout=timeout,
        )

    def search(self, keyword: str, limit: int = 10) -> List[ProductItem]:
        url = f"https://mobile.yangkeduo.com/search_result.html?search_key={quote(keyword)}"
        resp = self.session.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        items: List[ProductItem] = []
        for node in soup.select("[data-goods-id]")[:limit]:
            title_node = node.select_one(".title, .goods-name, h3")
            title = title_node.get_text(strip=True) if title_node else "拼多多商品"

            price_text = node.select_one(".price, .goods-price, .price-current")
            price = self._parse_price(price_text.get_text(strip=True) if price_text else "")

            sales_text = node.select_one(".sales, .goods-sales")
            sales = self._parse_sales(sales_text.get_text(strip=True) if sales_text else "0")

            shop_text = node.select_one(".shop-name, .mall-name")
            shop_name = shop_text.get_text(strip=True) if shop_text else "拼多多店铺"

            rating = 4.4

            goods_id = node.get("data-goods-id", "")
            href = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}" if goods_id else url

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
                    url=href,
                    fetched_at=datetime.now(),
                )
            )

        if not items:
            raise RuntimeError("拼多多页面未解析到商品，可能触发反爬或页面结构变更")
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
