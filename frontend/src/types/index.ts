export interface ProductItem {
  id: string;
  platform: "jd" | "taobao" | "pdd";
  keyword: string;
  title: string;
  price: number;
  sales: number;
  shop_name: string;
  shop_rating: number;
  url: string;
  fetched_at: string;
}

export interface SearchResponse {
  keyword: string;
  mode: "real" | "demo";
  degraded: boolean;
  logs: string[];
  total: number;
  items: ProductItem[];
  stats: {
    platform_distribution: Record<string, number>;
    price_range: { min: number; max: number; avg: number };
    value_top3: ProductItem[];
  };
}

export interface ExampleResponse {
  keyword: string;
  request: {
    keyword: string;
    platforms: string[];
    mode: string;
    limit: number;
  };
  response: SearchResponse;
}
