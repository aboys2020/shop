import { Package, TrendingDown, TrendingUp, Award } from "lucide-react";
import type { SearchResponse } from "@/types";

interface Props {
  result: SearchResponse;
}

export default function StatsCards({ result }: Props) {
  const { total, stats, mode, degraded } = result;
  const { min, max, avg } = stats.price_range;

  const dist = stats.platform_distribution;
  const platformText = Object.entries(dist)
    .map(([k, v]) => `${k.toUpperCase()}: ${v}`)
    .join(" / ");

  const cards = [
    {
      icon: Package,
      label: "采集总数",
      value: total,
      sub: degraded ? "已降级为演示数据" : `模式：${mode}`,
      color: "text-accent",
    },
    {
      icon: TrendingDown,
      label: "最低价格",
      value: `¥${min.toFixed(2)}`,
      sub: platformText || "—",
      color: "text-accent-2",
    },
    {
      icon: TrendingUp,
      label: "平均价格",
      value: `¥${avg.toFixed(2)}`,
      sub: `最高 ¥${max.toFixed(2)}`,
      color: "text-heading",
    },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-3">
      {cards.map((card, idx) => (
        <div
          key={card.label}
          className="card animate-fade-in-up flex items-start justify-between"
          style={{ animationDelay: `${0.1 * idx}s` }}
        >
          <div>
            <p className="text-xs text-muted">{card.label}</p>
            <p className={`mt-1 font-display text-2xl font-bold ${card.color}`}>{card.value}</p>
            <p className="mt-1 text-xs text-muted">{card.sub}</p>
          </div>
          <card.icon className={`h-6 w-6 ${card.color}`} />
        </div>
      ))}

      <div
        className="card animate-fade-in-up md:col-span-3"
        style={{ animationDelay: "0.3s" }}
      >
        <div className="mb-3 flex items-center gap-2">
          <Award className="h-4 w-4 text-accent" />
          <h3 className="font-display text-base font-semibold text-heading">性价比推荐 Top3</h3>
        </div>
        <div className="grid gap-3 md:grid-cols-3">
          {stats.value_top3.map((item, idx) => (
            <a
              key={item.id}
              href={item.url}
              target="_blank"
              rel="noreferrer"
              className="group rounded border border-border bg-bg p-3 transition-colors hover:border-accent"
            >
              <div className="mb-2 flex items-center justify-between">
                <span
                  className={`badge ${
                    item.platform === "jd"
                      ? "badge-jd"
                      : item.platform === "taobao"
                      ? "badge-taobao"
                      : "badge-pdd"
                  }`}
                >
                  {item.platform.toUpperCase()}
                </span>
                <span className="text-xs text-muted">#{idx + 1}</span>
              </div>
              <p className="line-clamp-2 text-sm text-heading group-hover:text-accent">
                {item.title}
              </p>
              <div className="mt-2 flex items-center justify-between text-xs text-muted">
                <span>¥{item.price.toFixed(2)}</span>
                <span>评分 {item.shop_rating}</span>
              </div>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}
