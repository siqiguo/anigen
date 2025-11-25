#!/bin/bash
# 启动 AniGen 服务器

cd "$(dirname "$0")"

# 激活虚拟环境
if [ -d "../venv" ]; then
    source ../venv/bin/activate
fi

# 启动服务器
python3 app.py

