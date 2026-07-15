import Header from "@/components/Header";
import SearchPanel from "@/components/SearchPanel";
import ExamplePanel from "@/components/ExamplePanel";
import StatsCards from "@/components/StatsCards";
import Charts from "@/components/Charts";
import ResultTable from "@/components/ResultTable";
import LogPanel from "@/components/LogPanel";
import { useAppStore } from "@/store/useAppStore";

export default function Home() {
  const { result, logs } = useAppStore();

  return (
    <div className="min-h-screen bg-bg pb-16">
      <Header />
      <main className="container mx-auto space-y-6 pt-6">
        <SearchPanel />
        <ExamplePanel />

        {result && (
          <div className="space-y-6">
            <StatsCards result={result} />
            <Charts result={result} />
            <ResultTable result={result} />
            <LogPanel logs={logs} />
          </div>
        )}
      </main>

      <footer className="container mx-auto mt-12 border-t border-border py-6 text-center text-xs text-muted">
        电商价格采集与对比工具 · 真实模式下可能受反爬限制，失败将自动降级为演示数据
      </footer>
    </div>
  );
}
