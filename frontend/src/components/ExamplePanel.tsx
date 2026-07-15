import { useEffect, useState } from "react";
import { ChevronDown, ChevronUp, Lightbulb } from "lucide-react";
import { useAppStore } from "@/store/useAppStore";

export default function ExamplePanel() {
  const { example, loadExample } = useAppStore();
  const [open, setOpen] = useState(true);

  useEffect(() => {
    loadExample();
  }, [loadExample]);

  if (!example) return null;

  return (
    <section className="card animate-fade-in-down" style={{ animationDelay: "0.2s" }}>
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex w-full items-center justify-between text-left"
      >
        <div className="flex items-center gap-2">
          <Lightbulb className="h-4 w-4 text-accent" />
          <h2 className="font-display text-lg font-semibold text-heading">
            示例：{example.keyword}
          </h2>
        </div>
        {open ? <ChevronUp className="h-4 w-4 text-muted" /> : <ChevronDown className="h-4 w-4 text-muted" />}
      </button>

      {open && (
        <div className="mt-4 space-y-4 border-t border-border pt-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded border border-border bg-bg p-3">
              <h3 className="mb-2 text-xs font-semibold text-accent-2">请求参数</h3>
              <pre className="overflow-x-auto text-xs text-muted">
                {JSON.stringify(example.request, null, 2)}
              </pre>
            </div>
            <div className="rounded border border-border bg-bg p-3">
              <h3 className="mb-2 text-xs font-semibold text-accent">结果摘要</h3>
              <ul className="space-y-1 text-xs text-muted">
                <li>模式：{example.response.mode}</li>
                <li>总条数：{example.response.total}</li>
                <li>
                  价格区间：¥{example.response.stats.price_range.min} ~ ¥
                  {example.response.stats.price_range.max}
                </li>
                <li>
                  平台分布：
                  {Object.entries(example.response.stats.platform_distribution)
                    .map(([k, v]) => `${k}: ${v}`)
                    .join("，")}
                </li>
              </ul>
            </div>
          </div>
          <p className="text-xs text-muted">
            上方为初始化示例。您可以在搜索区修改关键词并点击“运行采集”查看实时结果。
          </p>
        </div>
      )}
    </section>
  );
}
