#!/usr/bin/env python3
"""电商价格采集与对比工具命令行入口。"""

import argparse
import csv
import json
import sys
from pathlib import Path

from backend.services.search import run_search
from core.models import ProductItem


def main() -> int:
    parser = argparse.ArgumentParser(description="电商商品价格自动化采集与对比工具")
    parser.add_argument("--keyword", "-k", required=True, help="搜索关键词")
    parser.add_argument(
        "--platforms",
        "-p",
        default="jd,taobao,pdd",
        help="目标平台，逗号分隔，默认 jd,taobao,pdd",
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["real", "demo"],
        default="demo",
        help="运行模式：real 真实采集，demo 演示数据",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=10,
        help="每个平台采集数量，默认 10",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output",
        help="输出目录前缀，默认 output",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["csv", "json", "both"],
        default="both",
        help="输出格式",
    )
    parser.add_argument(
        "--chart",
        "-c",
        choices=["html", "png", "none"],
        default="html",
        help="是否生成图表",
    )

    args = parser.parse_args()
    platforms = [p.strip().lower() for p in args.platforms.split(",") if p.strip()]

    result = run_search(
        keyword=args.keyword,
        platforms=platforms,
        mode=args.mode,
        limit=args.limit,
    )

    print("\n".join(result["logs"]))
    print(f"\n共采集 {result['total']} 条商品，价格区间：{result['stats']['price_range']}")

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    base_name = f"{args.keyword.replace(' ', '_')}_{result['mode']}"

    items = result["items"]
    if args.format in ("json", "both"):
        json_path = out_dir / f"{base_name}.json"
        with open(json_path, "w", encoding="utf-8") as fp:
            json.dump(result, fp, ensure_ascii=False, indent=2)
        print(f"JSON 已保存: {json_path}")

    if args.format in ("csv", "both"):
        csv_path = out_dir / f"{base_name}.csv"
        _write_csv(csv_path, items)
        print(f"CSV 已保存: {csv_path}")

    if args.chart != "none" and items:
        # 懒加载图表库，轻量打包时可排除 plotly/matplotlib
        try:
            from core.visualizer import generate_charts
        except ImportError as exc:
            print(f"无法生成图表：{exc}")
            print("提示：当前为轻量构建，未包含图表库。如需图表请从源码安装完整依赖：pip install -r requirements.txt")
            return 1

        chart_path = out_dir / f"{base_name}_chart"
        product_items = [ProductItem.from_dict(item) for item in items]
        generated = generate_charts(
            items=product_items,
            output_path=str(chart_path),
            fmt=args.chart,
        )
        print(f"图表已保存: {generated}")

    return 0


def _write_csv(path: Path, items: list[dict]) -> None:
    if not items:
        return
    keys = list(items[0].keys())
    with open(path, "w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.DictWriter(fp, fieldnames=keys)
        writer.writeheader()
        writer.writerows(items)


if __name__ == "__main__":
    sys.exit(main())
