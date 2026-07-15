"""搜索服务：协调采集器与数据处理器。"""

from typing import Any, Dict, List

from core.models import ProductItem
from core.processor import compute_stats, process_items
from core.scrapers.factory import ScraperFactory


def run_search(
    keyword: str,
    platforms: List[str],
    mode: str = "real",
    limit: int = 10,
) -> Dict[str, Any]:
    """执行一次搜索，返回结果、统计与日志。"""
    logs: List[str] = []
    raw_items: List[ProductItem] = []
    degraded = False

    logs.append(f"开始搜索: keyword={keyword}, platforms={platforms}, mode={mode}")

    if mode == "demo":
        logs.append("使用演示数据模式")

    for platform in platforms:
        try:
            scraper = ScraperFactory.get_scraper(platform, mode=mode)
            logs.append(f"正在采集 {platform} ...")
            items = scraper.search(keyword, limit=limit)
            raw_items.extend(items)
            logs.append(f"{platform} 采集到 {len(items)} 条")
        except Exception as exc:
            logs.append(f"{platform} 采集失败: {exc}")

    if mode == "real" and not raw_items:
        logs.append("真实采集全部失败，自动降级到演示数据模式")
        degraded = True
        for platform in platforms:
            try:
                scraper = ScraperFactory.get_scraper(platform, mode="demo")
                items = scraper.search(keyword, limit=limit)
                raw_items.extend(items)
                logs.append(f"演示模式 {platform} 生成 {len(items)} 条")
            except Exception as exc:
                logs.append(f"演示模式 {platform} 也失败: {exc}")

    processed = process_items(raw_items)
    stats = compute_stats(processed)

    logs.append(f"清洗去重后共 {len(processed)} 条，按价格升序排列")

    return {
        "keyword": keyword,
        "mode": "demo" if degraded else mode,
        "degraded": degraded,
        "logs": logs,
        "total": len(processed),
        "items": [item.to_dict() for item in processed],
        "stats": stats,
    }
