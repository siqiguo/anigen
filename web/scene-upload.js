/**
 * 场景资源上传页面 - JavaScript
 */

const API_BASE_URL = "http://localhost:5001/api";

// 预设图片标签（场景视角）
const PRESET_IMAGE_LABELS = [
    { value: "front_view", label: "正面视角" },
    { value: "side_view", label: "侧面视角" },
    { value: "back_view", label: "背面视角" },
    { value: "top_view", label: "俯视图" },
    { value: "bottom_view", label: "仰视图" },
    { value: "wide_view", label: "广角视图" },
    { value: "close_view", label: "特写视图" },
    { value: "panoramic_view", label: "全景视图" },
    { value: "interior_view", label: "内部视角" },
    { value: "exterior_view", label: "外部视角" },
];

let imageCounter = 0;  // 用于生成唯一的图片项ID

class SceneUploadUI {
    constructor() {
        this.init();
    }

    init() {
        this.setupTabs();
        this.setupImageUploads();
        this.setupForm();
        this.setupList();
    }

    /**
     * 设置标签页
     */
    setupTabs() {
        const tabs = document.querySelectorAll(".tab");
        tabs.forEach(tab => {
            tab.addEventListener("click", () => {
                const tabName = tab.dataset.tab;
                
                // 更新标签状态
                tabs.forEach(t => t.classList.remove("active"));
                tab.classList.add("active");
                
                // 更新内容显示
                document.querySelectorAll(".tab-content").forEach(content => {
                    content.classList.remove("active");
                });
                document.getElementById(`${tabName}Tab`).classList.add("active");
                
                // 如果切换到列表页，加载场景列表
                if (tabName === "list") {
                    this.loadSceneList();
                }
            });
        });
    }

    /**
     * 设置图片上传功能
     */
    setupImageUploads() {
        const addImageBtn = document.getElementById("addImageBtn");
        addImageBtn.addEventListener("click", () => {
            this.addImageItem();
        });

        // 默认添加一个图片项
        this.addImageItem();
    }

    /**
     * 添加图片项
     */
    addImageItem() {
        const container = document.getElementById("imagesContainer");
        const itemId = `image_${imageCounter++}`;
        
        const item = document.createElement("div");
        item.className = "image-item";
        item.id = itemId;

        const header = document.createElement("div");
        header.className = "image-item-header";

        const labelDiv = document.createElement("div");
        labelDiv.className = "image-item-label";

        // 标签类型选择（预设/自定义）
        const labelTypeToggle = document.createElement("div");
        labelTypeToggle.className = "label-type-toggle";
        
        const presetBtn = document.createElement("button");
        presetBtn.type = "button";
        presetBtn.textContent = "预设标签";
        presetBtn.classList.add("active");
        presetBtn.dataset.type = "preset";
        
        const customBtn = document.createElement("button");
        customBtn.type = "button";
        customBtn.textContent = "自定义标签";
        customBtn.dataset.type = "custom";

        labelTypeToggle.appendChild(presetBtn);
        labelTypeToggle.appendChild(customBtn);

        // 预设标签选择
        const presetSelect = document.createElement("select");
        presetSelect.name = `${itemId}_label_preset`;
        presetSelect.className = "label-select";
        presetSelect.style.display = "block";
        
        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "请选择标签";
        presetSelect.appendChild(defaultOption);

        PRESET_IMAGE_LABELS.forEach(preset => {
            const option = document.createElement("option");
            option.value = preset.value;
            option.textContent = preset.label;
            presetSelect.appendChild(option);
        });

        // 自定义标签输入
        const customInput = document.createElement("input");
        customInput.type = "text";
        customInput.name = `${itemId}_label_custom`;
        customInput.className = "label-input";
        customInput.placeholder = "输入自定义标签";
        customInput.style.display = "none";

        labelDiv.appendChild(labelTypeToggle);
        labelDiv.appendChild(presetSelect);
        labelDiv.appendChild(customInput);

        // 删除按钮
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.className = "image-item-remove";
        removeBtn.textContent = "删除";
        removeBtn.addEventListener("click", () => {
            item.remove();
        });

        header.appendChild(labelDiv);
        header.appendChild(removeBtn);

        // 内容区域
        const content = document.createElement("div");
        content.className = "image-item-content";

        // 图片预览
        const previewDiv = document.createElement("div");
        const preview = document.createElement("img");
        preview.className = "image-item-preview";
        preview.style.display = "none";
        preview.alt = "图片预览";
        previewDiv.appendChild(preview);

        // 文件选择
        const fileInputWrapper = document.createElement("div");
        fileInputWrapper.className = "file-input-wrapper";
        
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.name = `${itemId}_file`;
        fileInput.accept = "image/*";
        fileInput.className = "file-input";
        fileInput.style.display = "none";

        const fileButton = document.createElement("label");
        fileButton.htmlFor = fileInput.id || `${itemId}_file_input`;
        fileButton.className = "file-input-button";
        fileButton.innerHTML = `<span>📷 选择图片</span>`;
        fileButton.style.cursor = "pointer";

        fileInput.id = `${itemId}_file_input`;
        fileButton.setAttribute("for", fileInput.id);

        fileInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (file) {
                fileButton.querySelector("span").textContent = file.name;
                fileButton.classList.add("has-file");
                
                // 显示预览
                const reader = new FileReader();
                reader.onload = (e) => {
                    preview.src = e.target.result;
                    preview.style.display = "block";
                };
                reader.readAsDataURL(file);
            }
        });

        fileInputWrapper.appendChild(fileInput);
        fileInputWrapper.appendChild(fileButton);

        const infoDiv = document.createElement("div");
        infoDiv.className = "image-item-info";
        infoDiv.appendChild(fileInputWrapper);

        content.appendChild(previewDiv);
        content.appendChild(infoDiv);

        // 标签类型切换
        presetBtn.addEventListener("click", () => {
            presetBtn.classList.add("active");
            customBtn.classList.remove("active");
            presetSelect.style.display = "block";
            customInput.style.display = "none";
        });

        customBtn.addEventListener("click", () => {
            customBtn.classList.add("active");
            presetBtn.classList.remove("active");
            presetSelect.style.display = "none";
            customInput.style.display = "block";
        });

        item.appendChild(header);
        item.appendChild(content);
        container.appendChild(item);
    }

    /**
     * 设置表单提交
     */
    setupForm() {
        const form = document.getElementById("sceneForm");
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            await this.submitScene();
        });
    }

    /**
     * 提交场景数据
     */
    async submitScene() {
        const form = document.getElementById("sceneForm");
        const formData = new FormData(form);
        const messageArea = document.getElementById("messageArea");
        const submitBtn = form.querySelector('button[type="submit"]');

        // 收集图片数据
        const imageItems = document.querySelectorAll(".image-item");
        const images = [];
        
        imageItems.forEach(item => {
            const fileInput = item.querySelector('input[type="file"]');
            const presetSelect = item.querySelector('.label-select');
            const customInput = item.querySelector('.label-input');
            const presetBtn = item.querySelector('button[data-type="preset"]');
            
            if (fileInput && fileInput.files.length > 0) {
                const file = fileInput.files[0];
                let label = "";
                
                // 判断使用预设还是自定义标签
                if (presetBtn && presetBtn.classList.contains("active")) {
                    label = presetSelect.value;
                } else {
                    label = customInput.value.trim();
                }
                
                if (label) {
                    images.push({
                        label: label,
                        file: file
                    });
                }
            }
        });

        if (images.length === 0) {
            messageArea.innerHTML = `
                <div class="error-message">
                    ❌ 请至少添加一张图片
                </div>
            `;
            return;
        }

        // 显示加载状态
        submitBtn.disabled = true;
        submitBtn.textContent = "上传中...";
        messageArea.innerHTML = "";

        try {
            // 添加基本表单数据
            const basicFormData = new FormData();
            basicFormData.append("name", formData.get("name") || "");
            basicFormData.append("description", formData.get("description") || "");
            basicFormData.append("location_type", formData.get("location_type") || "");
            basicFormData.append("time_of_day", formData.get("time_of_day") || "");
            basicFormData.append("weather", formData.get("weather") || "");
            basicFormData.append("mood", formData.get("mood") || "");
            basicFormData.append("style", formData.get("style") || "");
            basicFormData.append("tags", formData.get("tags") || "");

            // 添加图片数据
            images.forEach((img, index) => {
                basicFormData.append(`image_label_${index}`, img.label);
                basicFormData.append(`image_file_${index}`, img.file);
            });

            const response = await fetch(`${API_BASE_URL}/scenes`, {
                method: "POST",
                body: basicFormData
            });

            const result = await response.json();

            if (result.success) {
                messageArea.innerHTML = `
                    <div class="success-message">
                        ✅ 场景上传成功！场景ID: ${result.data.id}
                    </div>
                `;
                form.reset();
                this.resetImageInputs();
                
                // 切换到列表页显示新场景
                setTimeout(() => {
                    document.querySelector('.tab[data-tab="list"]').click();
                }, 1500);
            } else {
                messageArea.innerHTML = `
                    <div class="error-message">
                        ❌ 上传失败: ${result.error || "未知错误"}
                    </div>
                `;
            }
        } catch (error) {
            console.error("上传失败:", error);
            messageArea.innerHTML = `
                <div class="error-message">
                    ❌ 上传失败: ${error.message}
                    <br>请确保后端服务器正在运行 (http://localhost:5001)
                </div>
            `;
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "上传场景";
        }
    }

    /**
     * 重置图片输入
     */
    resetImageInputs() {
        const container = document.getElementById("imagesContainer");
        container.innerHTML = "";
        imageCounter = 0;
        // 重新添加一个空的图片项
        this.addImageItem();
    }

    /**
     * 设置列表功能
     */
    setupList() {
        const refreshBtn = document.getElementById("refreshBtn");
        refreshBtn.addEventListener("click", () => {
            this.loadSceneList();
        });

        const searchBtn = document.getElementById("searchBtn");
        searchBtn.addEventListener("click", () => {
            this.loadSceneList();
        });

        // 回车搜索
        const searchKeyword = document.getElementById("searchKeyword");
        searchKeyword.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                this.loadSceneList();
            }
        });
    }

    /**
     * 加载场景列表
     */
    async loadSceneList() {
        const listContainer = document.getElementById("sceneList");
        const loading = document.getElementById("listLoading");
        const keyword = document.getElementById("searchKeyword").value.trim();
        const locationType = document.getElementById("filterLocationType").value;
        const style = document.getElementById("filterStyle").value;

        loading.style.display = "block";
        listContainer.innerHTML = "";

        try {
            const params = new URLSearchParams();
            if (keyword) params.append("keyword", keyword);
            if (locationType) params.append("location_type", locationType);
            if (style) params.append("style", style);

            const url = `${API_BASE_URL}/scenes${params.toString() ? "?" + params.toString() : ""}`;
            const response = await fetch(url);
            const result = await response.json();

            if (result.success) {
                if (result.data.length === 0) {
                    listContainer.innerHTML = "<div class='loading'>暂无场景数据</div>";
                } else {
                    result.data.forEach(scene => {
                        listContainer.appendChild(this.createSceneCard(scene));
                    });
                }
            } else {
                listContainer.innerHTML = `
                    <div class="error-message">
                        ❌ 加载失败: ${result.error || "未知错误"}
                    </div>
                `;
            }
        } catch (error) {
            console.error("加载失败:", error);
            listContainer.innerHTML = `
                <div class="error-message">
                    ❌ 加载失败: ${error.message}
                    <br>请确保后端服务器正在运行 (http://localhost:5001)
                </div>
            `;
        } finally {
            loading.style.display = "none";
        }
    }

    /**
     * 创建场景卡片
     */
    createSceneCard(scene) {
        const card = document.createElement("div");
        card.className = "scene-card";

        const header = document.createElement("div");
        header.className = "scene-header";

        const name = document.createElement("div");
        name.className = "scene-name";
        name.textContent = scene.name;

        const actions = document.createElement("div");
        actions.className = "scene-actions";

        const viewBtn = document.createElement("button");
        viewBtn.className = "btn btn-small";
        viewBtn.textContent = "查看";
        viewBtn.addEventListener("click", () => {
            this.viewScene(scene);
        });

        const deleteBtn = document.createElement("button");
        deleteBtn.className = "btn btn-small";
        deleteBtn.textContent = "删除";
        deleteBtn.style.background = "#ef4444";
        deleteBtn.addEventListener("click", () => {
            if (confirm(`确定要删除场景 "${scene.name}" 吗？`)) {
                this.deleteScene(scene.id);
            }
        });

        actions.appendChild(viewBtn);
        actions.appendChild(deleteBtn);
        header.appendChild(name);
        header.appendChild(actions);

        const info = document.createElement("div");
        info.className = "scene-info";

        if (scene.description) {
            const descItem = document.createElement("div");
            descItem.className = "info-item";
            descItem.innerHTML = `
                <div class="info-label">描述</div>
                <div class="info-value">${scene.description}</div>
            `;
            info.appendChild(descItem);
        }

        if (scene.location_type) {
            const locationItem = document.createElement("div");
            locationItem.className = "info-item";
            locationItem.innerHTML = `
                <div class="info-label">场景类型</div>
                <div class="info-value">${scene.location_type}</div>
            `;
            info.appendChild(locationItem);
        }

        if (scene.time_of_day) {
            const timeItem = document.createElement("div");
            timeItem.className = "info-item";
            timeItem.innerHTML = `
                <div class="info-label">时间</div>
                <div class="info-value">${scene.time_of_day}</div>
            `;
            info.appendChild(timeItem);
        }

        if (scene.weather) {
            const weatherItem = document.createElement("div");
            weatherItem.className = "info-item";
            weatherItem.innerHTML = `
                <div class="info-label">天气</div>
                <div class="info-value">${scene.weather}</div>
            `;
            info.appendChild(weatherItem);
        }

        if (scene.mood) {
            const moodItem = document.createElement("div");
            moodItem.className = "info-item";
            moodItem.innerHTML = `
                <div class="info-label">氛围</div>
                <div class="info-value">${scene.mood}</div>
            `;
            info.appendChild(moodItem);
        }

        if (scene.style) {
            const styleItem = document.createElement("div");
            styleItem.className = "info-item";
            styleItem.innerHTML = `
                <div class="info-label">风格</div>
                <div class="info-value">${scene.style}</div>
            `;
            info.appendChild(styleItem);
        }

        if (scene.tags && scene.tags.length > 0) {
            const tagsItem = document.createElement("div");
            tagsItem.className = "info-item";
            tagsItem.innerHTML = `
                <div class="info-label">标签</div>
                <div class="info-value">${scene.tags.join(", ")}</div>
            `;
            info.appendChild(tagsItem);
        }

        // 图片预览
        const imagesDiv = document.createElement("div");
        imagesDiv.className = "scene-images";

        // 显示所有图片
        if (scene.images) {
            Object.entries(scene.images).forEach(([label, path]) => {
                const img = document.createElement("img");
                img.className = "scene-image";
                img.src = `${API_BASE_URL}/images/${path}`;
                img.alt = label;
                img.title = label;
                imagesDiv.appendChild(img);
            });
        }

        card.appendChild(header);
        card.appendChild(info);
        if (imagesDiv.children.length > 0) {
            card.appendChild(imagesDiv);
        }

        return card;
    }

    /**
     * 查看场景详情
     */
    viewScene(scene) {
        const details = [
            `ID: ${scene.id}`,
            `名称: ${scene.name}`,
            `描述: ${scene.description || "无"}`,
            `场景类型: ${scene.location_type || "无"}`,
            `时间: ${scene.time_of_day || "无"}`,
            `天气: ${scene.weather || "无"}`,
            `氛围: ${scene.mood || "无"}`,
            `风格: ${scene.style || "无"}`,
            `标签: ${scene.tags ? scene.tags.join(", ") : "无"}`,
        ].join("\n");

        alert(details);
    }

    /**
     * 删除场景
     */
    async deleteScene(sceneId) {
        try {
            const response = await fetch(`${API_BASE_URL}/scenes/${sceneId}`, {
                method: "DELETE"
            });

            const result = await response.json();

            if (result.success) {
                alert("场景删除成功");
                this.loadSceneList();
            } else {
                alert(`删除失败: ${result.error}`);
            }
        } catch (error) {
            console.error("删除失败:", error);
            alert(`删除失败: ${error.message}`);
        }
    }
}

// 页面加载完成后初始化
document.addEventListener("DOMContentLoaded", () => {
    new SceneUploadUI();
});

