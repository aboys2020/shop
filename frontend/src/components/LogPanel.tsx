import { Terminal } from "lucide-react";

interface Props {
  logs: string[];
}

export default function LogPanel({ logs }: Props) {
  if (!logs.length) return null;

  return (
    <div className="card animate-fade-in-up" style={{ animationDelay: "0.4s" }}>
      <div className="mb-3 flex items-center gap-2">
        <Terminal className="h-4 w-4 text-muted" />
        <h3 className="font-display text-sm font-semibold text-heading">运行日志</h3>
      </div>
      <div className="max-h-48 overflow-y-auto rounded border border-border bg-bg p-3 font-mono text-xs">
        {logs.map((log, idx) => (
          <div key={idx} className="mb-1 text-muted">
            <span className="mr-2 text-accent-2">&gt;</span>
            {log}
          </div>
        ))}
      </div>
    </div>
  );
}
