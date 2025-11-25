# 服务器设置说明

## 安装依赖

由于系统限制，请使用以下方式之一安装依赖：

### 方式1：使用虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r ../requirements.txt
```

### 方式2：使用 --break-system-packages（不推荐）

```bash
pip3 install --break-system-packages -r requirements.txt
```

### 方式3：使用 conda

```bash
conda create -n anigen python=3.10
conda activate anigen
pip install -r requirements.txt
```

## 启动服务器

```bash
cd server
python app.py
```

服务器将在 `http://localhost:5000` 启动。

## 测试随机角色生成

```bash
# 测试 API
curl -X POST http://localhost:5000/api/characters/random \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 访问前端

在浏览器中打开 `../web/character-upload.html`

