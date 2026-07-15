"""FastAPI 后端入口。"""

import os
import sys
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .services.search import run_search


def _get_app_dir() -> Path:
    """兼容源码运行与 PyInstaller 打包后的路径。"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


APP_DIR = _get_app_dir()
STATIC_DIR = APP_DIR / "backend" / "static"
if not STATIC_DIR.exists():
    STATIC_DIR = APP_DIR / "static"

app = FastAPI(title="电商价格采集与对比工具", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    keyword: str
    platforms: List[str]
    mode: str = "demo"
    limit: int = 10


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/example")
def example() -> dict:
    """返回初始化示例数据。"""
    keyword = "无线蓝牙耳机"
    request = {
        "keyword": keyword,
        "platforms": ["jd", "taobao", "pdd"],
        "mode": "demo",
        "limit": 6,
    }
    response = run_search(**request)
    return {"keyword": keyword, "request": request, "response": response}


@app.post("/api/search")
def search(payload: SearchRequest) -> dict:
    return run_search(
        keyword=payload.keyword,
        platforms=payload.platforms,
        mode=payload.mode,
        limit=payload.limit,
    )


# 静态文件服务：生产构建后的前端产物
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")


@app.get("/{full_path:path}")
def serve_spa(full_path: str) -> FileResponse:
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return FileResponse(APP_DIR / "placeholder.html")
