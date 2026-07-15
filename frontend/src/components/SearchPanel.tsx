import { Play, AlertCircle } from "lucide-react";
import { useAppStore } from "@/store/useAppStore";

const PLATFORM_OPTIONS = [
  { key: "jd", label: "京东" },
  { key: "taobao", label: "淘宝" },
  { key: "pdd", label: "拼多多" },
];

export default function SearchPanel() {
  const {
    keyword,
    platforms,
    mode,
    limit,
    loading,
    error,
    setKeyword,
    setMode,
    togglePlatform,
    setLimit,
    runSearch,
  } = useAppStore();

  return (
    <section className="card animate-fade-in-down space-y-5" style={{ animationDelay: "0.1s" }}>
      <div className="flex flex-col gap-4 md:flex-row md:items-end">
        <div className="flex-1">
          <label className="mb-1 block text-xs font-medium text-muted">搜索关键词</label>
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="例如：无线蓝牙耳机"
            className="input w-full"
            disabled={loading}
          />
        </div>

        <div>
          <label className="mb-1 block text-xs font-medium text-muted">数量 / 平台</label>
          <input
            type="number"
            min={1}
            max={30}
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
            className="input w-24"
            disabled={loading}
          />
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setMode(mode === "demo" ? "real" : "demo")}
            className={`rounded border px-4 py-2.5 text-sm font-medium transition-colors ${
              mode === "demo"
                ? "border-accent-2 text-accent-2 hover:bg-accent-2/10"
                : "border-danger text-danger hover:bg-danger/10"
            }`}
            disabled={loading}
          >
            {mode === "demo" ? "演示模式" : "真实采集"}
          </button>
          <button
            type="button"
            onClick={runSearch}
            disabled={loading}
            className="btn min-w-[120px]"
          >
            {loading ? (
              <span className="inline-flex items-center gap-2">
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                采集中
              </span>
            ) : (
              <>
                <Play className="h-4 w-4" /> 运行采集
              </>
            )}
          </button>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <span className="text-xs text-muted">目标平台：</span>
        {PLATFORM_OPTIONS.map((opt) => {
          const checked = platforms.includes(opt.key);
          return (
            <label
              key={opt.key}
              className={`flex cursor-pointer items-center gap-2 rounded border px-3 py-1.5 text-xs transition-colors ${
                checked
                  ? "border-accent bg-accent/10 text-accent"
                  : "border-border text-muted hover:text-heading"
              }`}
            >
              <input
                type="checkbox"
                className="h-3.5 w-3.5 accent-accent"
                checked={checked}
                onChange={() => togglePlatform(opt.key)}
                disabled={loading}
              />
              {opt.label}
            </label>
          );
        })}
      </div>

      {error && (
        <div className="flex items-center gap-2 rounded border border-danger/30 bg-danger/10 px-4 py-3 text-sm text-danger">
          <AlertCircle className="h-4 w-4" />
          {error}
        </div>
      )}
    </section>
  );
}
