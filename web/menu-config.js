/**
 * 菜单配置
 * 添加新页面时，只需在此文件中添加菜单项即可
 */

const menuConfig = [
    {
        title: "首页",
        icon: "🏠",
        url: "./index.html",
        id: "index"
    },
    {
        title: "分镜生成器",
        icon: "🎬",
        url: "./storyboard-generator.html",
        id: "storyboard-generator"
    },
    {
        title: "角色资源管理",
        icon: "🎭",
        url: "./character-upload.html",
        id: "character-upload"
    },
    {
        title: "场景资源管理",
        icon: "🏞️",
        url: "./scene-upload.html",
        id: "scene-upload"
    },
    {
        title: "Prompt 生成器",
        icon: "🎨",
        url: "./prompt-generator.html",
        id: "prompt-generator"
    }
];

/**
 * 根据当前页面路径获取当前菜单项ID
 */
function getCurrentPageId() {
    const path = window.location.pathname;
    const filename = path.split('/').pop() || 'index.html';
    
    // 从文件名提取ID（去掉.html后缀）
    const pageId = filename.replace('.html', '');
    
    // 检查是否在菜单配置中
    const menuItem = menuConfig.find(item => item.id === pageId);
    return menuItem ? menuItem.id : null;
}

/**
 * 渲染菜单
 */
function renderMenu() {
    const menuContainer = document.getElementById('sidebar-menu');
    if (!menuContainer) return;
    
    const currentPageId = getCurrentPageId();
    
    menuContainer.innerHTML = menuConfig.map(item => {
        const isActive = item.id === currentPageId;
        return `
            <a href="${item.url}" class="menu-item ${isActive ? 'active' : ''}">
                <span class="menu-icon">${item.icon}</span>
                <span class="menu-title">${item.title}</span>
            </a>
        `;
    }).join('');
}

/**
 * 初始化移动端菜单切换
 */
function initMobileMenu() {
    const toggleBtn = document.getElementById('mobile-menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (!toggleBtn || !sidebar) return;
    
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        if (overlay) {
            overlay.classList.toggle('active');
        }
    });
    
    if (overlay) {
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
    }
}

// 页面加载时自动渲染菜单
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        renderMenu();
        initMobileMenu();
    });
} else {
    renderMenu();
    initMobileMenu();
}

