/**
 * 角色资源上传页面 - JavaScript
 */

const API_BASE_URL = "http://localhost:5001/api";

// 预设图片标签
const PRESET_IMAGE_LABELS = [
    { value: "front_view", label: "正视图" },
    { value: "side_view", label: "侧视图" },
    { value: "back_view", label: "后视图" },
    { value: "expression_happy", label: "表情-开心" },
    { value: "expression_sad", label: "表情-悲伤" },
    { value: "expression_angry", label: "表情-愤怒" },
    { value: "expression_surprised", label: "表情-惊讶" },
    { value: "expression_neutral", label: "表情-中性/平静" },
    { value: "expression_scared", label: "表情-害怕" },
    { value: "expression_excited", label: "表情-兴奋" },
    { value: "expression_confused", label: "表情-困惑" },
];

let imageCounter = 0;  // 用于生成唯一的图片项ID

class CharacterUploadUI {
    constructor() {
        this.init();
    }

    init() {
        this.setupTabs();
        this.setupImageUploads();
        this.setupForm();
        this.setupList();
        this.setupRandomGenerator();
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
                
                // 如果切换到列表页，加载角色列表
                if (tabName === "list") {
                    this.loadCharacterList();
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
        const form = document.getElementById("characterForm");
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            await this.submitCharacter();
        });
    }

    /**
     * 提交角色数据
     */
    async submitCharacter() {
        const form = document.getElementById("characterForm");
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
            basicFormData.append("appearance", formData.get("appearance") || "");
            basicFormData.append("personality", formData.get("personality") || "");
            basicFormData.append("age", formData.get("age") || "");
            basicFormData.append("gender", formData.get("gender") || "");
            basicFormData.append("style", formData.get("style") || "");
            basicFormData.append("tags", formData.get("tags") || "");

            // 添加图片数据
            images.forEach((img, index) => {
                basicFormData.append(`image_label_${index}`, img.label);
                basicFormData.append(`image_file_${index}`, img.file);
            });

            const response = await fetch(`${API_BASE_URL}/characters`, {
                method: "POST",
                body: basicFormData
            });

            const result = await response.json();

            if (result.success) {
                messageArea.innerHTML = `
                    <div class="success-message">
                        ✅ 角色上传成功！角色ID: ${result.data.id}
                    </div>
                `;
                form.reset();
                this.resetImageInputs();
                
                // 切换到列表页显示新角色
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
            submitBtn.textContent = "上传角色";
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
     * 设置随机生成功能
     */
    setupRandomGenerator() {
        const randomBtn = document.getElementById("randomBtn");
        randomBtn.addEventListener("click", () => {
            this.generateRandomCharacter();
        });
    }

    /**
     * 生成随机角色
     */
    async generateRandomCharacter() {
        const randomBtn = document.getElementById("randomBtn");
        const preview = document.getElementById("randomCharacterPreview");
        const content = document.getElementById("randomCharacterContent");
        const messageArea = document.getElementById("messageArea");

        randomBtn.disabled = true;
        randomBtn.textContent = "生成中...";
        preview.style.display = "none";
        messageArea.innerHTML = "";

        try {
            const response = await fetch(`${API_BASE_URL}/characters/random`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    generate_image: false
                })
            });

            const result = await response.json();

            if (result.success) {
                const charData = result.data.character;
                const prompts = result.data.prompts;

                // 填充表单
                document.getElementById("name").value = charData.name;
                document.getElementById("description").value = charData.description;
                document.getElementById("appearance").value = charData.appearance;
                document.getElementById("personality").value = charData.personality;
                document.getElementById("age").value = charData.age || "";
                document.getElementById("gender").value = charData.gender || "";
                document.getElementById("style").value = charData.style || "";
                document.getElementById("tags").value = charData.tags.join(", ");

                // 显示预览
                content.innerHTML = `
                    <div class="character-info" style="margin-top: 1rem;">
                        <div class="info-item">
                            <div class="info-label">名称</div>
                            <div class="info-value">${charData.name}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">外观</div>
                            <div class="info-value">${charData.appearance}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">性格</div>
                            <div class="info-value">${charData.personality}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">风格</div>
                            <div class="info-value">${charData.style}</div>
                        </div>
                    </div>
                    <div style="margin-top: 1rem;">
                        <p><strong>提示：</strong>表单已自动填充，您可以修改后上传，或使用 Prompt 生成器生成图片。</p>
                        <button class="btn btn-small" style="margin-top: 0.5rem;" onclick="window.open('prompt-generator.html', '_blank')">
                            打开 Prompt 生成器生成图片
                        </button>
                    </div>
                `;
                preview.style.display = "block";

                messageArea.innerHTML = `
                    <div class="success-message">
                        ✅ 随机角色生成成功！表单已自动填充。
                    </div>
                `;
            } else {
                messageArea.innerHTML = `
                    <div class="error-message">
                        ❌ 生成失败: ${result.error || "未知错误"}
                    </div>
                `;
            }
        } catch (error) {
            console.error("生成失败:", error);
            messageArea.innerHTML = `
                <div class="error-message">
                    ❌ 生成失败: ${error.message}
                    <br>请确保后端服务器正在运行 (http://localhost:5000)
                </div>
            `;
        } finally {
            randomBtn.disabled = false;
            randomBtn.textContent = "🎲 随机生成角色";
        }
    }

    /**
     * 设置列表功能
     */
    setupList() {
        const refreshBtn = document.getElementById("refreshBtn");
        refreshBtn.addEventListener("click", () => {
            this.loadCharacterList();
        });

        const searchBtn = document.getElementById("searchBtn");
        searchBtn.addEventListener("click", () => {
            this.loadCharacterList();
        });

        // 回车搜索
        const searchKeyword = document.getElementById("searchKeyword");
        searchKeyword.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                this.loadCharacterList();
            }
        });
    }

    /**
     * 加载角色列表
     */
    async loadCharacterList() {
        const listContainer = document.getElementById("characterList");
        const loading = document.getElementById("listLoading");
        const keyword = document.getElementById("searchKeyword").value.trim();
        const style = document.getElementById("filterStyle").value;

        loading.style.display = "block";
        listContainer.innerHTML = "";

        try {
            const params = new URLSearchParams();
            if (keyword) params.append("keyword", keyword);
            if (style) params.append("style", style);

            const url = `${API_BASE_URL}/characters${params.toString() ? "?" + params.toString() : ""}`;
            const response = await fetch(url);
            const result = await response.json();

            if (result.success) {
                if (result.data.length === 0) {
                    listContainer.innerHTML = "<div class='loading'>暂无角色数据</div>";
                } else {
                    result.data.forEach(character => {
                        listContainer.appendChild(this.createCharacterCard(character));
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
                    <br>请确保后端服务器正在运行 (http://localhost:5000)
                </div>
            `;
        } finally {
            loading.style.display = "none";
        }
    }

    /**
     * 创建角色卡片
     */
    createCharacterCard(character) {
        const card = document.createElement("div");
        card.className = "character-card";

        const header = document.createElement("div");
        header.className = "character-header";

        const name = document.createElement("div");
        name.className = "character-name";
        name.textContent = character.name;

        const actions = document.createElement("div");
        actions.className = "character-actions";

        const viewBtn = document.createElement("button");
        viewBtn.className = "btn btn-small";
        viewBtn.textContent = "查看";
        viewBtn.addEventListener("click", () => {
            this.viewCharacter(character);
        });

        const deleteBtn = document.createElement("button");
        deleteBtn.className = "btn btn-small";
        deleteBtn.textContent = "删除";
        deleteBtn.style.background = "#ef4444";
        deleteBtn.addEventListener("click", () => {
            if (confirm(`确定要删除角色 "${character.name}" 吗？`)) {
                this.deleteCharacter(character.id);
            }
        });

        actions.appendChild(viewBtn);
        actions.appendChild(deleteBtn);
        header.appendChild(name);
        header.appendChild(actions);

        const info = document.createElement("div");
        info.className = "character-info";

        if (character.description) {
            const descItem = document.createElement("div");
            descItem.className = "info-item";
            descItem.innerHTML = `
                <div class="info-label">描述</div>
                <div class="info-value">${character.description}</div>
            `;
            info.appendChild(descItem);
        }

        if (character.appearance) {
            const appearanceItem = document.createElement("div");
            appearanceItem.className = "info-item";
            appearanceItem.innerHTML = `
                <div class="info-label">外观</div>
                <div class="info-value">${character.appearance}</div>
            `;
            info.appendChild(appearanceItem);
        }

        if (character.style) {
            const styleItem = document.createElement("div");
            styleItem.className = "info-item";
            styleItem.innerHTML = `
                <div class="info-label">风格</div>
                <div class="info-value">${character.style}</div>
            `;
            info.appendChild(styleItem);
        }

        if (character.tags && character.tags.length > 0) {
            const tagsItem = document.createElement("div");
            tagsItem.className = "info-item";
            tagsItem.innerHTML = `
                <div class="info-label">标签</div>
                <div class="info-value">${character.tags.join(", ")}</div>
            `;
            info.appendChild(tagsItem);
        }

        // 图片预览
        const imagesDiv = document.createElement("div");
        imagesDiv.className = "character-images";

        // 显示所有图片（新格式）
        if (character.images) {
            Object.entries(character.images).forEach(([label, path]) => {
                const img = document.createElement("img");
                img.className = "character-image";
                img.src = `${API_BASE_URL}/images/${path}`;
                img.alt = label;
                img.title = label;
                imagesDiv.appendChild(img);
            });
        } else {
            // 向后兼容：显示旧格式的图片
            if (character.front_view) {
                const img = document.createElement("img");
                img.className = "character-image";
                img.src = `${API_BASE_URL}/images/${character.front_view}`;
                img.alt = "前视图";
                img.title = "前视图";
                imagesDiv.appendChild(img);
            }

            if (character.side_view) {
                const img = document.createElement("img");
                img.className = "character-image";
                img.src = `${API_BASE_URL}/images/${character.side_view}`;
                img.alt = "侧视图";
                img.title = "侧视图";
                imagesDiv.appendChild(img);
            }

            if (character.back_view) {
                const img = document.createElement("img");
                img.className = "character-image";
                img.src = `${API_BASE_URL}/images/${character.back_view}`;
                img.alt = "后视图";
                img.title = "后视图";
                imagesDiv.appendChild(img);
            }

            if (character.expressions) {
                Object.entries(character.expressions).forEach(([key, path]) => {
                    const expr = STANDARD_EXPRESSIONS.find(e => e.key === key);
                    const img = document.createElement("img");
                    img.className = "character-image";
                    img.src = `${API_BASE_URL}/images/${path}`;
                    img.alt = expr ? expr.name : key;
                    img.title = expr ? expr.name : key;
                    imagesDiv.appendChild(img);
                });
            }
        }

        card.appendChild(header);
        card.appendChild(info);
        if (imagesDiv.children.length > 0) {
            card.appendChild(imagesDiv);
        }

        return card;
    }

    /**
     * 查看角色详情
     */
    viewCharacter(character) {
        const details = [
            `ID: ${character.id}`,
            `名称: ${character.name}`,
            `描述: ${character.description || "无"}`,
            `外观: ${character.appearance}`,
            `性格: ${character.personality || "无"}`,
            `年龄: ${character.age || "无"}`,
            `性别: ${character.gender || "无"}`,
            `风格: ${character.style || "无"}`,
            `标签: ${character.tags ? character.tags.join(", ") : "无"}`,
        ].join("\n");

        alert(details);
    }

    /**
     * 删除角色
     */
    async deleteCharacter(characterId) {
        try {
            const response = await fetch(`${API_BASE_URL}/characters/${characterId}`, {
                method: "DELETE"
            });

            const result = await response.json();

            if (result.success) {
                alert("角色删除成功");
                this.loadCharacterList();
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
    new CharacterUploadUI();
});

