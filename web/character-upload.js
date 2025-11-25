/**
 * 角色资源上传页面 - JavaScript
 */

const API_BASE_URL = "http://localhost:5000/api";

// 标准表情列表
const STANDARD_EXPRESSIONS = [
    { key: "happy", name: "开心" },
    { key: "sad", name: "悲伤" },
    { key: "angry", name: "愤怒" },
    { key: "surprised", name: "惊讶" },
    { key: "neutral", name: "中性/平静" },
    { key: "scared", name: "害怕" },
    { key: "excited", name: "兴奋" },
    { key: "confused", name: "困惑" },
];

class CharacterUploadUI {
    constructor() {
        this.init();
    }

    init() {
        this.setupTabs();
        this.setupFileUploads();
        this.setupExpressions();
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
     * 设置文件上传预览
     */
    setupFileUploads() {
        const fileInputs = ["front_view", "side_view", "back_view"];
        
        fileInputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            const label = document.getElementById(`${inputId}_label`);
            const nameSpan = document.getElementById(`${inputId}_name`);
            const preview = document.getElementById(`${inputId}_preview`);
            
            input.addEventListener("change", (e) => {
                const file = e.target.files[0];
                if (file) {
                    nameSpan.textContent = file.name;
                    label.classList.add("has-file");
                    
                    // 显示预览
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        preview.src = e.target.result;
                        preview.style.display = "block";
                    };
                    reader.readAsDataURL(file);
                } else {
                    nameSpan.textContent = "";
                    label.classList.remove("has-file");
                    preview.style.display = "none";
                }
            });
        });
    }

    /**
     * 设置表情上传区域
     */
    setupExpressions() {
        const container = document.getElementById("expressionsUpload");
        container.innerHTML = "";

        STANDARD_EXPRESSIONS.forEach(expr => {
            const item = document.createElement("div");
            item.className = "expression-upload-item";

            const label = document.createElement("label");
            label.className = "file-upload-label";
            label.textContent = expr.name;

            const inputWrapper = document.createElement("div");
            inputWrapper.className = "file-input-wrapper";

            const input = document.createElement("input");
            input.type = "file";
            input.name = `expression_${expr.key}`;
            input.id = `expression_${expr.key}`;
            input.accept = "image/*";
            input.className = "file-input";

            const inputButton = document.createElement("label");
            inputButton.htmlFor = `expression_${expr.key}`;
            inputButton.className = "file-input-button";
            inputButton.innerHTML = `<span>📷 选择图片</span>`;

            input.addEventListener("change", (e) => {
                const file = e.target.files[0];
                if (file) {
                    inputButton.classList.add("has-file");
                    inputButton.querySelector("span").textContent = file.name;
                } else {
                    inputButton.classList.remove("has-file");
                    inputButton.querySelector("span").textContent = "📷 选择图片";
                }
            });

            inputWrapper.appendChild(input);
            inputWrapper.appendChild(inputButton);
            item.appendChild(label);
            item.appendChild(inputWrapper);
            container.appendChild(item);
        });
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

        // 显示加载状态
        submitBtn.disabled = true;
        submitBtn.textContent = "上传中...";
        messageArea.innerHTML = "";

        try {
            const response = await fetch(`${API_BASE_URL}/characters`, {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                messageArea.innerHTML = `
                    <div class="success-message">
                        ✅ 角色上传成功！角色ID: ${result.data.id}
                    </div>
                `;
                form.reset();
                this.resetFileInputs();
                
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
                    <br>请确保后端服务器正在运行 (http://localhost:5000)
                </div>
            `;
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "上传角色";
        }
    }

    /**
     * 重置文件输入
     */
    resetFileInputs() {
        const fileInputs = ["front_view", "side_view", "back_view"];
        fileInputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            const label = document.getElementById(`${inputId}_label`);
            const nameSpan = document.getElementById(`${inputId}_name`);
            const preview = document.getElementById(`${inputId}_preview`);
            
            input.value = "";
            nameSpan.textContent = "";
            label.classList.remove("has-file");
            preview.style.display = "none";
        });

        // 重置表情输入
        document.querySelectorAll('input[name^="expression_"]').forEach(input => {
            input.value = "";
            const button = input.nextElementSibling;
            if (button) {
                button.classList.remove("has-file");
                button.querySelector("span").textContent = "📷 选择图片";
            }
        });
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

