/**
 * 分镜生成器前端脚本
 */

const API_BASE_URL = 'http://localhost:5001';

// DOM元素
const scriptTextarea = document.getElementById('script-text');
const scriptTitleInput = document.getElementById('script-title');
const preferResourcesCheckbox = document.getElementById('prefer-resources');
const generateBtn = document.getElementById('generate-btn');
const clearBtn = document.getElementById('clear-btn');
const resourcesPreview = document.getElementById('resources-preview');
const resourcesGrid = document.getElementById('resources-grid');
const storyboardSection = document.getElementById('storyboard-section');
const storyboardStats = document.getElementById('storyboard-stats');
const shotsList = document.getElementById('shots-list');
const loading = document.getElementById('loading');
const loadingDetail = document.getElementById('loading-detail');
const progressBar = document.getElementById('progress');
const errorMessage = document.getElementById('error-message');
const copyJsonBtn = document.getElementById('copy-json-btn');
const downloadJsonBtn = document.getElementById('download-json-btn');

let currentStoryboard = null;

// 事件监听
generateBtn.addEventListener('click', handleGenerate);
clearBtn.addEventListener('click', handleClear);
copyJsonBtn.addEventListener('click', handleCopyJson);
downloadJsonBtn.addEventListener('click', handleDownloadJson);

/**
 * 处理生成分镜
 */
async function handleGenerate() {
    const scriptText = scriptTextarea.value.trim();
    if (!scriptText) {
        showError('请输入剧本文本');
        return;
    }

    // 显示加载状态
    showLoading('正在解析剧本...');
    hideError();
    hideResults();

    try {
        const preferResources = preferResourcesCheckbox.checked;
        const title = scriptTitleInput.value.trim() || undefined;

        // 更新进度
        updateProgress(20, '正在解析剧本...');

        // 生成分镜脚本
        const response = await fetch(`${API_BASE_URL}/api/storyboard/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                script_text: scriptText,
                title: title,
                prefer_existing_resources: preferResources,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '生成分镜脚本失败');
        }

        updateProgress(80, '正在处理结果...');

        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error || '生成分镜脚本失败');
        }

        updateProgress(100, '完成！');

        // 显示结果
        setTimeout(() => {
            displayStoryboard(result.data);
            if (preferResources) {
                displayResources(result.data);
            }
            hideLoading();
        }, 500);

    } catch (error) {
        console.error('生成分镜脚本失败:', error);
        hideLoading();
        
        // 提供更详细的错误信息
        let errorMsg = `生成失败: ${error.message}`;
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            errorMsg = `连接失败: 无法连接到服务器 (${API_BASE_URL})<br>
                        <small>请确保：<br>
                        1. 服务器正在运行 (cd server && python app.py)<br>
                        2. 服务器地址正确 (当前: ${API_BASE_URL})<br>
                        3. 如果使用file://打开页面，请改用HTTP服务器访问</small>`;
        }
        showError(errorMsg);
    }
}

/**
 * 显示分镜结果
 */
function displayStoryboard(storyboardData) {
    currentStoryboard = storyboardData;
    
    // 显示统计信息
    const metadata = storyboardData.metadata || {};
    storyboardStats.innerHTML = `
        <div class="stat-item">
            <div class="stat-label">总镜头数</div>
            <div class="stat-value">${metadata.total_shots || 0}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">总时长</div>
            <div class="stat-value">${(metadata.total_duration || 0).toFixed(1)}秒</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">标题</div>
            <div class="stat-value" style="font-size: 1rem;">${storyboardData.title || '未命名'}</div>
        </div>
    `;

    // 显示镜头列表
    const shots = storyboardData.storyboard || [];
    shotsList.innerHTML = shots.map((shot, index) => createShotCard(shot, index)).join('');

    storyboardSection.style.display = 'block';
}

/**
 * 创建镜头卡片
 */
function createShotCard(shot, index) {
    const resources = [];
    
    if (shot.scene_resource) {
        resources.push({
            type: 'scene',
            name: shot.scene_resource.resource_name,
            score: shot.scene_resource.match_score
        });
    }
    
    if (shot.character_resources && shot.character_resources.length > 0) {
        shot.character_resources.forEach(ref => {
            resources.push({
                type: 'character',
                name: ref.resource_name,
                score: ref.match_score
            });
        });
    }
    
    if (shot.prop_resources && shot.prop_resources.length > 0) {
        shot.prop_resources.forEach(ref => {
            resources.push({
                type: 'prop',
                name: ref.resource_name,
                score: ref.match_score
            });
        });
    }
    
    if (shot.action_resources && shot.action_resources.length > 0) {
        shot.action_resources.forEach(ref => {
            resources.push({
                type: 'action',
                name: ref.resource_name,
                score: ref.match_score
            });
        });
    }

    const resourcesHtml = resources.length > 0
        ? `
            <div class="shot-resources">
                <div class="shot-resources-title">使用的资源：</div>
                ${resources.map(r => `
                    <span class="resource-tag ${r.type}">
                        ${r.type === 'scene' ? '🏞️' : r.type === 'character' ? '👤' : r.type === 'prop' ? '🎒' : '🎬'}
                        ${r.name} ${r.score ? `(${(r.score * 100).toFixed(0)}%)` : ''}
                    </span>
                `).join('')}
            </div>
        `
        : '';

    return `
        <div class="shot-card">
            <div class="shot-header">
                <div class="shot-title">镜头 ${shot.shot_number}</div>
                <div class="shot-meta">
                    <span>场景 ${shot.scene_number}</span>
                    <span>${shot.shot_type}</span>
                    <span>${shot.duration}秒</span>
                </div>
            </div>
            <div class="shot-content">
                <div class="shot-description">${escapeHtml(shot.description)}</div>
                ${shot.dialogue ? `<div style="margin-top: 0.5rem; padding: 0.75rem; background: var(--surface); border-radius: 6px; font-style: italic; color: var(--text-secondary);">💬 ${escapeHtml(shot.dialogue)}</div>` : ''}
                ${shot.characters && shot.characters.length > 0 ? `<div style="margin-top: 0.5rem; font-size: 0.875rem; color: var(--text-secondary);">角色: ${shot.characters.join(', ')}</div>` : ''}
                ${resourcesHtml}
            </div>
        </div>
    `;
}

/**
 * 显示资源匹配结果
 */
function displayResources(storyboardData) {
    const shots = storyboardData.storyboard || [];
    const resources = new Map();

    // 收集所有使用的资源
    shots.forEach(shot => {
        if (shot.scene_resource) {
            const key = `scene_${shot.scene_resource.resource_id}`;
            if (!resources.has(key)) {
                resources.set(key, {
                    type: 'scene',
                    ...shot.scene_resource
                });
            }
        }
        
        if (shot.character_resources) {
            shot.character_resources.forEach(ref => {
                const key = `character_${ref.resource_id}`;
                if (!resources.has(key)) {
                    resources.set(key, {
                        type: 'character',
                        ...ref
                    });
                }
            });
        }
        
        if (shot.prop_resources) {
            shot.prop_resources.forEach(ref => {
                const key = `prop_${ref.resource_id}`;
                if (!resources.has(key)) {
                    resources.set(key, {
                        type: 'prop',
                        ...ref
                    });
                }
            });
        }
        
        if (shot.action_resources) {
            shot.action_resources.forEach(ref => {
                const key = `action_${ref.resource_id}`;
                if (!resources.has(key)) {
                    resources.set(key, {
                        type: 'action',
                        ...ref
                    });
                }
            });
        }
    });

    if (resources.size === 0) {
        resourcesPreview.style.display = 'none';
        return;
    }

    resourcesGrid.innerHTML = Array.from(resources.values()).map(resource => {
        const typeLabels = {
            scene: '场景',
            character: '角色',
            prop: '道具',
            action: '动作'
        };
        
        const typeIcons = {
            scene: '🏞️',
            character: '👤',
            prop: '🎒',
            action: '🎬'
        };

        return `
            <div class="resource-card">
                <div class="resource-card-header">
                    <h4>${typeIcons[resource.type]} ${escapeHtml(resource.resource_name)}</h4>
                    <span class="resource-badge ${resource.type}">${typeLabels[resource.type]}</span>
                </div>
                <div class="resource-info">
                    ${resource.match_score ? `<div>匹配度: ${(resource.match_score * 100).toFixed(0)}%</div>` : ''}
                    ${resource.match_reason ? `<div style="margin-top: 0.25rem; font-size: 0.8rem; color: var(--text-secondary);">${escapeHtml(resource.match_reason)}</div>` : ''}
                </div>
            </div>
        `;
    }).join('');

    resourcesPreview.style.display = 'block';
}

/**
 * 处理清空
 */
function handleClear() {
    scriptTextarea.value = '';
    scriptTitleInput.value = '';
    hideResults();
    hideError();
}

/**
 * 处理复制JSON
 */
async function handleCopyJson() {
    if (!currentStoryboard) {
        showError('没有可复制的数据');
        return;
    }

    try {
        const jsonText = JSON.stringify(currentStoryboard, null, 2);
        await navigator.clipboard.writeText(jsonText);
        
        copyJsonBtn.textContent = '✓ 已复制';
        copyJsonBtn.classList.add('copied');
        setTimeout(() => {
            copyJsonBtn.textContent = '📋 复制JSON';
            copyJsonBtn.classList.remove('copied');
        }, 2000);
    } catch (error) {
        console.error('复制失败:', error);
        showError('复制失败，请手动复制');
    }
}

/**
 * 处理下载JSON
 */
function handleDownloadJson() {
    if (!currentStoryboard) {
        showError('没有可下载的数据');
        return;
    }

    const jsonText = JSON.stringify(currentStoryboard, null, 2);
    const blob = new Blob([jsonText], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `storyboard_${currentStoryboard.title || 'untitled'}_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/**
 * 显示加载状态
 */
function showLoading(message) {
    loading.style.display = 'block';
    loadingDetail.textContent = message || '正在处理...';
    generateBtn.disabled = true;
}

/**
 * 隐藏加载状态
 */
function hideLoading() {
    loading.style.display = 'none';
    generateBtn.disabled = false;
}

/**
 * 更新进度
 */
function updateProgress(percent, message) {
    progressBar.style.width = `${percent}%`;
    if (message) {
        loadingDetail.textContent = message;
    }
}

/**
 * 显示错误消息
 */
function showError(message) {
    errorMessage.innerHTML = message;
    errorMessage.style.display = 'block';
}

/**
 * 隐藏错误消息
 */
function hideError() {
    errorMessage.style.display = 'none';
}

/**
 * 隐藏结果
 */
function hideResults() {
    storyboardSection.style.display = 'none';
    resourcesPreview.style.display = 'none';
}

/**
 * HTML转义
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

