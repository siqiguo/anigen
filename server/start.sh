#!/bin/bash
# 启动 AniGen 资源管理 API 服务器

echo "启动 AniGen 资源管理 API 服务器..."
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python 3"
    exit 1
fi

# 检查依赖
if ! python3 -c "import flask" 2>/dev/null; then
    echo "安装依赖..."
    pip3 install -r requirements.txt
fi

# 启动服务器
cd "$(dirname "$0")"
python3 app.py

