import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import type { SearchResponse } from "@/types";

interface Props {
  result: SearchResponse;
}

const COLORS = ["#FF9F1C", "#2EC4B6", "#E71D36"];

export default function Charts({ result }: Props) {
  const { items, stats } = result;

  const platformData = Object.entries(stats.platform_distribution).map(([name, value]) => ({
    name: name.toUpperCase(),
    value,
  }));

  const priceBuckets: Record<string, number> = {};
  items.forEach((item) => {
    const bucket = Math.floor(item.price / 50) * 50;
    const label = `¥${bucket}-${bucket + 50}`;
    priceBuckets[label] = (priceBuckets[label] || 0) + 1;
  });
  const priceData = Object.entries(priceBuckets).map(([name, value]) => ({ name, value }));

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="card animate-fade-in-up" style={{ animationDelay: "0.1s" }}>
        <h3 className="mb-4 font-display text-sm font-semibold text-heading">平台分布</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={platformData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
              >
                {platformData.map((entry, index) => (
                  <Cell key={`cell-${entry.name}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1F2833",
                  border: "1px solid #3A4555",
                  borderRadius: "6px",
                }}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
        <h3 className="mb-4 font-display text-sm font-semibold text-heading">价格区间分布</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={priceData}>
              <XAxis dataKey="name" tick={{ fill: "#8D99AE", fontSize: 10 }} />
              <YAxis tick={{ fill: "#8D99AE", fontSize: 10 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1F2833",
                  border: "1px solid #3A4555",
                  borderRadius: "6px",
                }}
              />
              <Bar dataKey="value" fill="#2EC4B6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
