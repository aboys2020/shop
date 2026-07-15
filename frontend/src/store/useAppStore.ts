import { create } from "zustand";
import type { ExampleResponse, SearchResponse } from "@/types";

interface AppState {
  keyword: string;
  platforms: string[];
  mode: "real" | "demo";
  limit: number;
  loading: boolean;
  result: SearchResponse | null;
  example: ExampleResponse | null;
  logs: string[];
  error: string | null;
  setKeyword: (keyword: string) => void;
  setMode: (mode: "real" | "demo") => void;
  togglePlatform: (platform: string) => void;
  setLimit: (limit: number) => void;
  loadExample: () => Promise<void>;
  runSearch: () => Promise<void>;
}

const API_BASE = "";

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const resp = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(text || `请求失败: ${resp.status}`);
  }
  return resp.json() as Promise<T>;
}

export const useAppStore = create<AppState>((set, get) => ({
  keyword: "机械键盘",
  platforms: ["jd", "taobao", "pdd"],
  mode: "demo",
  limit: 8,
  loading: false,
  result: null,
  example: null,
  logs: [],
  error: null,

  setKeyword: (keyword) => set({ keyword }),
  setMode: (mode) => set({ mode }),
  togglePlatform: (platform) => {
    const { platforms } = get();
    if (platforms.includes(platform)) {
      set({ platforms: platforms.filter((p) => p !== platform) });
    } else {
      set({ platforms: [...platforms, platform] });
    }
  },
  setLimit: (limit) => set({ limit }),

  loadExample: async () => {
    try {
      const data = await fetchJson<ExampleResponse>("/api/example");
      set({ example: data, result: data.response, logs: data.response.logs });
    } catch (err) {
      set({ error: err instanceof Error ? err.message : "加载示例失败" });
    }
  },

  runSearch: async () => {
    const { keyword, platforms, mode, limit } = get();
    if (!keyword.trim()) {
      set({ error: "请输入关键词" });
      return;
    }
    if (platforms.length === 0) {
      set({ error: "请至少选择一个平台" });
      return;
    }
    set({ loading: true, error: null, result: null, logs: [] });
    try {
      const data = await fetchJson<SearchResponse>("/api/search", {
        method: "POST",
        body: JSON.stringify({ keyword, platforms, mode, limit }),
      });
      set({ result: data, logs: data.logs, loading: false });
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : "请求失败",
        loading: false,
      });
    }
  },
}));
