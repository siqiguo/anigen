# Web 界面说明

## 页面结构

所有页面都使用统一的布局，包含左侧菜单栏和主内容区域。

## 添加新页面

### 1. 创建 HTML 文件

在 `web/` 目录下创建新的 HTML 文件，例如 `new-page.html`。

### 2. 使用标准布局结构

在 HTML 文件中使用以下结构：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>页面标题 - AniGen</title>
    <link rel="stylesheet" href="./styles.css">
</head>
<body>
    <!-- 应用布局 -->
    <div class="app-layout">
        <!-- 移动端菜单按钮 -->
        <button id="mobile-menu-toggle" class="mobile-menu-toggle">☰</button>
        
        <!-- 侧边栏遮罩（移动端） -->
        <div id="sidebar-overlay" class="sidebar-overlay"></div>
        
        <!-- 侧边栏 -->
        <aside id="sidebar" class="sidebar">
            <div class="sidebar-header">
                <h1 class="sidebar-logo">🎬 AniGen</h1>
                <p class="sidebar-subtitle">AI动画生成系统</p>
            </div>
            <nav id="sidebar-menu" class="sidebar-menu">
                <!-- 菜单项将通过 menu-config.js 动态生成 -->
            </nav>
        </aside>
        
        <!-- 主内容区域 -->
        <main class="main-content-wrapper">
            <div class="container">
                <!-- 你的页面内容 -->
            </div>
        </main>
    </div>

    <script src="./menu-config.js"></script>
    <script src="./your-script.js"></script>
</body>
</html>
```

### 3. 更新菜单配置

在 `menu-config.js` 中添加新菜单项：

```javascript
const menuConfig = [
    // ... 现有菜单项
    {
        title: "新页面",
        icon: "🎯",
        url: "./new-page.html",
        id: "new-page"
    }
];
```

**注意：**
- `id` 应该与 HTML 文件名（去掉 `.html` 后缀）一致
- `url` 是相对于当前文件的路径
- `icon` 可以使用任何 emoji 或图标

### 4. 完成

保存文件后，新页面会自动出现在左侧菜单栏中，并且当前页面会被高亮显示。

## 菜单配置说明

`menu-config.js` 文件包含所有页面的菜单配置。每次添加新页面时，只需：

1. 在 `menuConfig` 数组中添加新的菜单项对象
2. 确保 `id` 与 HTML 文件名匹配
3. 菜单会自动更新，当前页面会自动高亮

## 响应式设计

- **桌面端**：侧边栏固定在左侧，始终可见
- **移动端**：侧边栏默认隐藏，点击菜单按钮（☰）显示/隐藏

## 样式定制

所有样式都在 `styles.css` 中定义，使用 CSS 变量便于主题定制：

- `--primary-color`: 主色调
- `--sidebar-width`: 侧边栏宽度（默认 260px）
- `--background`: 背景色
- `--surface`: 卡片/表面颜色

## 现有页面

1. **首页** (`index.html`) - 欢迎页面，展示系统功能和工作流程
2. **分镜生成器** (`storyboard-generator.html`) - 从剧本生成分镜脚本
3. **角色资源管理** (`character-upload.html`) - 上传和管理角色资源
4. **Prompt 生成器** (`prompt-generator.html`) - 生成 Nano Banana 图片生成 prompt
