# Nano Banana Prompt 生成器 - 前端页面

这是一个用于生成 Nano Banana AI 图像生成 prompt 的前端工具页面。

## 功能特性

- ✅ 简洁直观的表单界面
- ✅ 自动生成三视图 prompt（前视图、侧视图、后视图）
- ✅ 自动生成多种表情 prompt（8种标准表情）
- ✅ 支持自定义表情选择
- ✅ 一键复制单个 prompt
- ✅ 一键复制所有 prompt
- ✅ **直接调用 Gemini 3.0 API 生成图片**（需 API Key）
- ✅ 图片预览和下载功能
- ✅ 响应式设计，支持移动端

## 使用方法

### 1. 打开页面

直接在浏览器中打开 `prompt-generator.html` 文件即可使用。

### 2. 填写角色信息

在表单中填写以下信息：

- **外观描述**（必填）：详细描述角色的外观特征
  - 例如：`年轻男性，黑色短发，蓝色眼睛，穿着冒险者服装，棕色皮靴，腰间挂着剑`
  
- **年龄**（可选）：角色的年龄
  
- **性别**（可选）：角色的性别
  
- **风格**（必填）：选择角色的艺术风格
  - Anime（二次元）
  - Cartoon（卡通）
  - Realistic（写实）
  - 3D
  - Pixar

- **需要生成的表情**：选择需要生成的表情（默认全选）
  - 开心 (happy)
  - 悲伤 (sad)
  - 愤怒 (angry)
  - 惊讶 (surprised)
  - 中性/平静 (neutral)
  - 害怕 (scared)
  - 兴奋 (excited)
  - 困惑 (confused)

### 3. 生成 Prompt

点击"生成 Prompt"按钮，系统会自动生成所有需要的 prompt。

### 4. 复制 Prompt

- **复制单个 prompt**：点击每个 prompt 卡片右上角的"复制"按钮
- **复制全部 prompt**：点击输出区域顶部的"复制全部"按钮

### 5. 生成图片（可选）

如果输入了 Gemini API Key，可以点击"生成图片"按钮直接调用 Gemini 3.0 API 生成图片：

1. **获取 API Key**：
   - 访问 [Google AI Studio](https://aistudio.google.com/apikey)
   - 创建并复制您的 API Key

2. **输入 API Key**：
   - 在表单的"Gemini API Key"字段中输入您的 API Key

3. **生成图片**：
   - 生成 Prompt 后，点击"生成图片"按钮
   - 系统会自动为每个 prompt 生成对应的图片
   - 生成完成后可以预览和下载图片

**注意**：
- 由于浏览器 CORS 限制，直接调用 API 可能会失败
- 如果遇到 CORS 错误，建议：
  - 使用后端代理服务器
  - 或使用 Google AI Studio 网页版手动生成
  - 或配置 CORS 代理

## 文件结构

```
web/
├── prompt-generator.html  # 主页面
├── prompt-generator.js    # JavaScript 逻辑
├── styles.css             # 样式文件
└── README.md              # 本文件
```

## 技术实现

- **纯前端实现**：无需后端服务器，可直接在浏览器中运行
- **原生 JavaScript**：不依赖任何框架，轻量高效
- **响应式设计**：使用 CSS Grid 和 Flexbox，适配各种屏幕尺寸
- **现代 UI**：使用 CSS 变量和现代设计风格

## 示例

### 输入示例

```
外观描述: 年轻女性，银色长发，紫色眼睛，穿着魔法师袍，手持法杖
年龄: 22
性别: 女
风格: Anime（二次元）
表情: 全选
```

### 输出示例

生成的 prompt 包括：

1. **前视图 (Front View)**
2. **侧视图 (Side View)**
3. **后视图 (Back View)**
4. **开心 (happy)**
5. **悲伤 (sad)**
6. **愤怒 (angry)**
7. **惊讶 (surprised)**
8. **中性/平静 (neutral)**
9. **害怕 (scared)**
10. **兴奋 (excited)**
11. **困惑 (confused)**

每个 prompt 都是完整的、可直接用于 Nano Banana API 的文本。

## 注意事项

1. **外观描述要详细**：越详细的描述，生成的 prompt 质量越高
2. **保持一致性**：所有 prompt 会自动使用相同的角色描述，确保生成的角色图片一致
3. **风格选择**：选择合适的风格会影响生成图片的艺术风格
4. **表情选择**：可以根据实际需求选择需要的表情，不必全部生成
5. **API Key 安全**：API Key 仅存储在浏览器本地，不会上传到服务器
6. **CORS 限制**：直接调用 Gemini API 可能因浏览器 CORS 限制而失败，建议使用后端代理
7. **API 费用**：使用 Gemini API 生成图片可能产生费用，请查看 Google Cloud 定价页面

## 浏览器兼容性

- Chrome/Edge（推荐）
- Firefox
- Safari
- 移动端浏览器

需要支持以下现代 Web API：
- Clipboard API（用于复制功能）
- ES6+ JavaScript 特性

## 与后端集成

如果需要与后端 Python 代码集成，可以参考 `src/assets/prompt_generator.py` 中的实现。

前端 JavaScript 版本与后端 Python 版本的 prompt 生成逻辑保持一致。

