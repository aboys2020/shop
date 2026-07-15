#!/usr/bin/env python3
"""一键启动后端服务。"""

import sys

import uvicorn


def main() -> int:
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
