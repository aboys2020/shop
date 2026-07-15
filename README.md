# 电商价格采集与对比工具

一站式电商商品价格自动化采集与横向对比工具。支持通过关键词从京东、淘宝、拼多多批量采集商品名称、价格、销量、店铺评分与链接，完成数据清洗去重、按价格排序、性价比推荐，并以表格与图表形式展示。

项目同时提供：

- **命令行工具（CLI）**：可直接运行，输出 CSV/JSON/HTML 图表。
- **Web 演示页**：输入关键词后在线运行采集脚本，实时查看结果与可视化。
- **演示数据模式**：无需真实请求电商平台，即可生成完整示例与结果。

---

## 目录结构

```
/workspace/
├── .trae/documents/          # PRD 与技术架构文档
├── README.md                 # 本文件
├── requirements.txt          # Python 依赖
├── run.py                    # 一键启动 Web 服务
├── cli.py                    # 命令行入口
├── backend/                  # FastAPI 后端
│   ├── main.py               # API 与静态文件服务
│   ├── services/search.py    # 搜索服务
│   └── static/               # 前端构建产物
├── core/                     # 核心采集与处理层（CLI 与 Web 共用）
│   ├── models.py             # 统一数据模型
│   ├── processor.py          # 清洗 / 去重 / 排序 / 评分
│   ├── visualizer.py         # CLI 图表生成
│   └── scrapers/             # 各平台采集器 + 演示数据生成器
└── frontend/                 # React + Vite + Tailwind 前端
    ├── src/
    │   ├── components/       # 页面组件
    │   ├── pages/Home.tsx    # 首页
    │   └── store/useAppStore.ts  # Zustand 状态管理
    └── package.json
```

---

## 安装依赖

### Python

```bash
pip install -r requirements.txt
```

### 前端（如需要二次开发）

```bash
cd frontend
pnpm install
```

---

## 命令行工具 CLI

### 快速使用（演示模式）

```bash
python cli.py --keyword 机械键盘 --mode demo --limit 8
```

### 参数说明

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--keyword` | `-k` | 必填 | 搜索关键词 |
| `--platforms` | `-p` | `jd,taobao,pdd` | 目标平台，逗号分隔 |
| `--mode` | `-m` | `demo` | `real` 真实采集 / `demo` 演示数据 |
| `--limit` | `-l` | `10` | 每个平台采集数量 |
| `--output` | `-o` | `output` | 输出目录 |
| `--format` | `-f` | `both` | `csv` / `json` / `both` |
| `--chart` | `-c` | `html` | `html` / `png` / `none` |

### 示例

```bash
# 导出 CSV + JSON + HTML 图表
python cli.py --keyword 无线蓝牙耳机 --mode demo --limit 10 --format both --chart html

# 仅导出 CSV，不生成图表
python cli.py --keyword 鼠标 --platforms jd,pdd --mode demo --format csv --chart none

# 尝试真实采集（无有效 Cookie 时会自动降级为演示模式）
python cli.py --keyword 手机壳 --mode real --limit 5
```

---

## Web 演示页

### 一键启动

```bash
python run.py
```

服务默认运行在 [http://localhost:8000](http://localhost:8000)。

### 开发模式（热更新）

1. 启动后端：

```bash
python run.py
```

2. 在另一个终端启动前端开发服务器：

```bash
cd frontend
pnpm run dev
```

前端开发服务器通常运行在 [http://localhost:5173](http://localhost:5173)，API 请求会通过 Vite 代理转发到后端。

### 生产构建

```bash
cd frontend
pnpm run build
```

构建产物会自动输出到 `backend/static/`，随后通过 `python run.py` 即可直接 serving。

---

## 核心 API

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/example` | GET | 初始化示例数据 |
| `/api/search` | POST | 执行采集，参数：`keyword`, `platforms`, `mode`, `limit` |
| `/docs` | GET | FastAPI 自动生成的 Swagger 文档 |

---

## 打包为可执行文件

### 自动打包（GitHub Actions）

仓库已配置 [`.github/workflows/build.yml`](.github/workflows/build.yml)，推送到 GitHub 后会自动在 Windows 环境下构建并上传 exe：

```bash
git push origin main
```

构建产物位于 GitHub Actions 的 `windows-executables` Artifacts 中。推送 `v*` 标签还会自动创建 Release：

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 本地手动打包

1. 构建前端：

```bash
cd frontend
pnpm install
pnpm run build
```

2. 安装 PyInstaller：

```bash
pip install pyinstaller
```

3. 打包轻量 CLI（无图表、无 Web 框架，体积最小）：

```bash
pip install -r requirements-cli-light.txt
pyinstaller packaging/cli-light.spec
```

4. 打包 Web 服务（含前端静态文件）：

```bash
pip install -r requirements-web.txt
pyinstaller packaging/web.spec
```

产物在 `dist/` 目录：

```
dist/
├── price_scraper_cli.exe   # 轻量 CLI
└── price_scraper_web.exe   # Web 服务
```

### 体积优化说明

- 轻量 CLI 已移除 `pandas`、`numpy`、`matplotlib`、`plotly` 以及 `fastapi`/`uvicorn` 等 Web 框架依赖。
- Web 服务已移除 `pandas`、`numpy`、`matplotlib`、`plotly`，前端图表由 React + Recharts 实现。
- GitHub Actions 构建时启用 UPX 压缩，可进一步减小 exe 体积。
- 受限于 Python 解释器本身，再压缩也难以低于 10–15 MB。

---

## 架构说明

- **前端演示层**：React 18 + Vite + Tailwind CSS + Recharts，深色数据仪表盘风格。
- **后端 API 层**：FastAPI，提供 `/api/search` 与 `/api/example`，并 serving 前端静态文件。
- **核心采集与处理层**：
  - `core/scrapers/`：京东、淘宝、拼多多真实采集器 + 演示数据生成器。
  - `core/processor.py`：清洗、去重、按价格升序排序、性价比评分。
  - `core/visualizer.py`：CLI 模式下生成 Plotly/Matplotlib 图表。

CLI 与 Web 共用 `core/` 与 `backend/services/search.py`，避免逻辑重复。

---

## 真实采集说明

由于京东、淘宝、拼多多均具备较强的反爬与登录校验机制，在默认无有效 Cookie/登录态的环境下，真实模式通常会失败。系统设计为：

- 单平台失败不影响其他平台。
- 若真实模式全部失败，自动降级为演示数据模式，并标记 `degraded=true`。
- 演示数据按各平台特征生成价格、销量、店铺评分等字段，保证工具始终可运行与演示。

如需生产环境真实采集，请自行补充：代理池、Cookie/登录态、浏览器自动化（如 Playwright/Selenium）以及符合各平台服务条款的访问策略。

---

## 初始化示例

Web 首页首次加载时会自动调用 `/api/example`，以“无线蓝牙耳机”为关键词展示示例请求参数与结果，包括：

- 价格从低到高排列的商品表格
- 平台分布饼图
- 价格区间柱状图
- 性价比 Top3 推荐卡片
- 运行日志

用户可直接在搜索区修改关键词并点击“运行采集”查看实时结果。
