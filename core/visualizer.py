"""CLI 图表生成。"""

import json
import os
from typing import Any, Dict, List

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .models import ProductItem
from .processor import compute_stats


def generate_charts(
    items: List[ProductItem],
    output_path: str,
    fmt: str = "html",
) -> str:
    """生成图表文件，返回最终文件路径。"""
    stats = compute_stats(items)
    prices = [item.price for item in items]
    platforms = [item.platform for item in items]

    if fmt == "html":
        return _render_html(items, stats, prices, platforms, output_path)
    return _render_png(items, stats, prices, platforms, output_path)


def _render_html(
    items: List[ProductItem],
    stats: Dict[str, Any],
    prices: List[float],
    platforms: List[str],
    output_path: str,
) -> str:
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("价格分布", "平台占比", "性价比 Top5", "价格箱线图"),
        specs=[
            [{"type": "histogram"}, {"type": "pie"}],
            [{"type": "bar"}, {"type": "box"}],
        ],
    )

    fig.add_trace(go.Histogram(x=prices, nbinsx=10, marker_color="#2EC4B6"), row=1, col=1)

    dist = stats["platform_distribution"]
    fig.add_trace(
        go.Pie(labels=list(dist.keys()), values=list(dist.values()), marker_colors=["#FF9F1C", "#2EC4B6", "#E71D36"]),
        row=1,
        col=2,
    )

    top5 = sorted(
        items,
        key=lambda x: (x.shop_rating * x.sales**0.5) / max(x.price, 0.01),
        reverse=True,
    )[:5]
    fig.add_trace(
        go.Bar(
            x=[item.title[:15] + "..." for item in top5],
            y=[(item.shop_rating * item.sales**0.5) / max(item.price, 0.01) for item in top5],
            marker_color="#FF9F1C",
        ),
        row=2,
        col=1,
    )

    fig.add_trace(go.Box(x=platforms, y=prices, marker_color="#2EC4B6"), row=2, col=2)

    fig.update_layout(
        title_text=f"电商价格对比分析（共 {len(items)} 条）",
        template="plotly_dark",
        showlegend=False,
        height=700,
    )

    if not output_path.endswith(".html"):
        output_path += ".html"
    fig.write_html(output_path, include_plotlyjs="cdn")
    return output_path


def _render_png(
    items: List[ProductItem],
    stats: Dict[str, Any],
    prices: List[float],
    platforms: List[str],
    output_path: str,
) -> str:
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"电商价格对比分析（共 {len(items)} 条）", fontsize=14)

    axes[0, 0].hist(prices, bins=10, color="#2EC4B6", edgecolor="black")
    axes[0, 0].set_title("价格分布")
    axes[0, 0].set_xlabel("价格")
    axes[0, 0].set_ylabel("数量")

    dist = stats["platform_distribution"]
    axes[0, 1].pie(dist.values(), labels=dist.keys(), autopct="%1.1f%%", colors=["#FF9F1C", "#2EC4B6", "#E71D36"])
    axes[0, 1].set_title("平台占比")

    top5 = sorted(
        items,
        key=lambda x: (x.shop_rating * x.sales**0.5) / max(x.price, 0.01),
        reverse=True,
    )[:5]
    axes[1, 0].barh(
        [item.title[:15] + "..." for item in top5],
        [(item.shop_rating * item.sales**0.5) / max(item.price, 0.01) for item in top5],
        color="#FF9F1C",
    )
    axes[1, 0].set_title("性价比 Top5")
    axes[1, 0].invert_yaxis()

    axes[1, 1].boxplot([prices], labels=["价格"])
    axes[1, 1].set_title("价格箱线图")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    if not output_path.endswith(".png"):
        output_path += ".png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path
