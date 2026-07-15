export default function Header() {
  return (
    <header className="animate-fade-in-down border-b border-border bg-surface/50 py-8">
      <div className="container mx-auto">
        <h1 className="font-display text-4xl font-bold tracking-tight text-heading md:text-5xl">
          电商价格<span className="text-accent">采集</span>与对比
        </h1>
        <p className="mt-3 max-w-2xl text-sm text-muted">
          一站式商品价格自动化采集工具。支持京东、淘宝、拼多多关键词搜索，自动清洗去重、按价格排序，并提供横向对比与性价比推荐。
        </p>
      </div>
    </header>
  );
}
