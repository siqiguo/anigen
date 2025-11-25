# 故障排除指南

## "Failed to fetch" 错误

### 问题原因
这个错误通常表示前端无法连接到后端服务器。

### 解决方案

#### 1. 检查服务器是否运行
```bash
# 检查端口5001是否有服务
lsof -ti:5001

# 如果没有，启动服务器
cd server
python app.py
```

#### 2. 检查端口配置
- 前端配置: `web/storyboard-generator.js` 中的 `API_BASE_URL = 'http://localhost:5001'`
- 服务器端口: `server/app.py` 中默认端口为 5001

#### 3. 如果使用 file:// 协议打开页面
浏览器可能会阻止 file:// 协议访问 localhost。解决方法：

**方法1: 使用HTTP服务器（推荐）**
```bash
# 在项目根目录启动简单的HTTP服务器
cd /Users/guosq/workspace/claude-workspace/anigen
python3 -m http.server 8080

# 然后在浏览器访问
# http://localhost:8080/web/storyboard-generator.html
```

**方法2: 修改浏览器设置（不推荐）**
- Chrome: 启动时添加 `--disable-web-security` 标志（仅用于开发）

#### 4. 检查代理设置
如果系统配置了代理，可能会影响 localhost 连接：
```bash
# 测试连接（绕过代理）
curl --noproxy localhost http://localhost:5001/
```

#### 5. 检查防火墙
确保防火墙没有阻止本地连接。

### 测试服务器连接

```bash
# 测试服务器是否响应
curl http://localhost:5001/

# 测试分镜生成API
curl -X POST http://localhost:5001/api/storyboard/generate \
  -H "Content-Type: application/json" \
  -d '{"script_text":"测试","prefer_existing_resources":false}'
```

### 常见错误信息

1. **"Failed to fetch"**
   - 服务器未运行
   - 端口不匹配
   - CORS问题（使用file://打开）

2. **"NetworkError"**
   - 网络连接问题
   - 代理配置问题

3. **"生成失败: 剧本文本不能为空"**
   - 这是正常的验证错误，请检查输入

## 其他问题

### 服务器启动失败
```bash
# 检查Python版本（需要3.10+）
python --version

# 检查依赖是否安装
pip install -r requirements.txt

# 检查端口是否被占用
lsof -ti:5001
```

### 资源匹配不工作
- 确保资源库中有资源
- 检查资源描述是否足够详细
- 尝试降低匹配阈值

