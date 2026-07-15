import { ExternalLink } from "lucide-react";
import type { SearchResponse } from "@/types";

interface Props {
  result: SearchResponse;
}

function formatNumber(n: number): string {
  return n.toLocaleString("zh-CN");
}

export default function ResultTable({ result }: Props) {
  const { items } = result;

  return (
    <div className="card animate-fade-in-up overflow-hidden" style={{ animationDelay: "0.3s" }}>
      <div className="mb-4 flex items-center justify-between">
        <h3 className="font-display text-base font-semibold text-heading">按价格从低到高排序</h3>
        <span className="text-xs text-muted">共 {items.length} 条</span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-border text-muted">
              <th className="pb-3 pl-2 font-medium">平台</th>
              <th className="pb-3 font-medium">商品名称</th>
              <th className="pb-3 font-medium">店铺</th>
              <th className="pb-3 font-medium">价格</th>
              <th className="pb-3 font-medium">销量</th>
              <th className="pb-3 font-medium">评分</th>
              <th className="pb-3 pr-2 font-medium">链接</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, idx) => (
              <tr
                key={item.id}
                className="border-b border-border/50 transition-colors hover:bg-surface-2/50"
                style={{ animationDelay: `${idx * 0.03}s` }}
              >
                <td className="py-3 pl-2">
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
                </td>
                <td className="max-w-xs py-3 pr-4">
                  <p className="truncate text-heading" title={item.title}>
                    {item.title}
                  </p>
                </td>
                <td className="py-3 text-muted">{item.shop_name}</td>
                <td className="py-3 font-medium text-accent-2">
                  ¥{item.price.toFixed(2)}
                </td>
                <td className="py-3 text-muted">{formatNumber(item.sales)}</td>
                <td className="py-3 text-muted">{item.shop_rating.toFixed(2)}</td>
                <td className="py-3 pr-2">
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-accent hover:underline"
                  >
                    查看 <ExternalLink className="h-3 w-3" />
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
