/**
 * Nano Banana Prompt 生成器 - 前端实现
 */

// 标准表情列表
const STANDARD_EXPRESSIONS = [
    "happy",
    "sad",
    "angry",
    "surprised",
    "neutral",
    "scared",
    "excited",
    "confused",
];

// 表情中文名称映射
const EXPRESSION_NAMES = {
    happy: "开心",
    sad: "悲伤",
    angry: "愤怒",
    surprised: "惊讶",
    neutral: "中性/平静",
    scared: "害怕",
    excited: "兴奋",
    confused: "困惑",
};

// 表情描述映射
const EXPRESSION_DESCRIPTIONS = {
    happy: "happy, joyful, smiling expression. Eyes should be bright and cheerful, mouth showing a genuine smile",
    sad: "sad, melancholic expression. Eyes should look downcast or teary, mouth slightly downturned",
    angry: "angry, furious expression. Eyebrows furrowed, eyes narrowed or glaring, mouth showing anger",
    surprised: "surprised, shocked expression. Eyes wide open, eyebrows raised, mouth open in an 'O' shape",
    neutral: "neutral, calm, expressionless expression. Eyes looking straight ahead, relaxed facial features, mouth in a neutral position",
    scared: "scared, frightened expression. Eyes wide with fear, eyebrows raised, mouth slightly open",
    excited: "excited, enthusiastic expression. Eyes bright and wide, eyebrows raised, mouth open in a big smile or cheer",
    confused: "confused, puzzled expression. Eyes looking slightly off to the side, one eyebrow raised, mouth slightly open",
};

// Prompt 生成器类
class PromptGenerator {
    constructor(defaultStyle = "anime") {
        this.defaultStyle = defaultStyle;
    }

    /**
     * 构建完整的角色描述字符串
     */
    buildCharacterDescription(data) {
        const parts = [];

        if (data.appearance) {
            parts.push(data.appearance);
        }

        if (data.age) {
            parts.push(`${data.age} years old`);
        }

        if (data.gender) {
            parts.push(data.gender);
        }

        const style = data.style || this.defaultStyle;
        if (style) {
            parts.push(`${style} style`);
        }

        return parts.join(", ");
    }

    /**
     * 生成前视图 prompt
     */
    generateFrontViewPrompt(data) {
        const description = this.buildCharacterDescription(data);
        const style = data.style || this.defaultStyle;

        return `Create a front view character design sheet illustration of: ${description}

Requirements:
- Full body front view, character facing forward
- White or transparent background
- Consistent character design with detailed appearance
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: ${style}`;
    }

    /**
     * 生成侧视图 prompt
     */
    generateSideViewPrompt(data) {
        const description = this.buildCharacterDescription(data);
        const style = data.style || this.defaultStyle;

        return `Create a side view character design sheet illustration of: ${description}

Requirements:
- Full body side view (profile), character facing left or right
- White or transparent background
- Must match the front view character design exactly (same clothing, appearance, proportions)
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: ${style}`;
    }

    /**
     * 生成后视图 prompt
     */
    generateBackViewPrompt(data) {
        const description = this.buildCharacterDescription(data);
        const style = data.style || this.defaultStyle;

        return `Create a back view character design sheet illustration of: ${description}

Requirements:
- Full body back view, character facing away
- White or transparent background
- Must match the front and side view character design exactly (same clothing, appearance, proportions)
- High quality, clean line art or rendered illustration
- Character should be centered and clearly visible
- Style: ${style}`;
    }

    /**
     * 生成表情 prompt
     */
    generateExpressionPrompt(data, expressionName) {
        const description = this.buildCharacterDescription(data);
        const style = data.style || this.defaultStyle;

        if (!EXPRESSION_DESCRIPTIONS[expressionName]) {
            throw new Error(`Unknown expression: ${expressionName}`);
        }

        const expressionDesc = EXPRESSION_DESCRIPTIONS[expressionName];

        return `Create a character portrait of: ${description}

Requirements:
- Character showing a ${expressionDesc}
- Upper body or close-up portrait view
- White or transparent background
- Must match the character design from the three-view sheets exactly
- Facial expression should be clear and expressive
- High quality, clean line art or rendered illustration
- Style: ${style}`;
    }

    /**
     * 生成所有 prompt
     */
    generateAllPrompts(data, selectedExpressions) {
        const prompts = {};

        // 三视图
        prompts.front_view = {
            title: "前视图 (Front View)",
            prompt: this.generateFrontViewPrompt(data),
        };
        prompts.side_view = {
            title: "侧视图 (Side View)",
            prompt: this.generateSideViewPrompt(data),
        };
        prompts.back_view = {
            title: "后视图 (Back View)",
            prompt: this.generateBackViewPrompt(data),
        };

        // 表情
        const expressions = selectedExpressions || STANDARD_EXPRESSIONS;
        expressions.forEach(exprName => {
            try {
                prompts[`expression_${exprName}`] = {
                    title: `${EXPRESSION_NAMES[exprName]} (${exprName})`,
                    prompt: this.generateExpressionPrompt(data, exprName),
                };
            } catch (error) {
                console.warn(`Failed to generate prompt for expression: ${exprName}`, error);
            }
        });

        return prompts;
    }
}

// UI 管理类
class PromptGeneratorUI {
    constructor() {
        this.generator = new PromptGenerator();
        this.init();
    }

    init() {
        this.setupForm();
        this.setupExpressions();
        this.setupEventListeners();
    }

    /**
     * 设置表单
     */
    setupForm() {
        const form = document.getElementById("characterForm");
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        const clearBtn = document.getElementById("clearBtn");
        clearBtn.addEventListener("click", () => {
            this.clearForm();
        });
    }

    /**
     * 设置表情复选框
     */
    setupExpressions() {
        const grid = document.getElementById("expressionsGrid");
        grid.innerHTML = "";

        STANDARD_EXPRESSIONS.forEach(expr => {
            const label = document.createElement("label");
            label.className = "checkbox-label";
            
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.name = "expressions";
            checkbox.value = expr;
            checkbox.checked = true; // 默认全选
            
            const span = document.createElement("span");
            span.textContent = EXPRESSION_NAMES[expr];
            
            label.appendChild(checkbox);
            label.appendChild(span);
            grid.appendChild(label);
        });
    }

    /**
     * 设置事件监听器
     */
    setupEventListeners() {
        const copyAllBtn = document.getElementById("copyAllBtn");
        copyAllBtn.addEventListener("click", () => {
            this.copyAllPrompts();
        });

        const generateImagesBtn = document.getElementById("generateImagesBtn");
        generateImagesBtn.addEventListener("click", () => {
            this.generateImages();
        });

        const downloadAllBtn = document.getElementById("downloadAllBtn");
        downloadAllBtn.addEventListener("click", () => {
            this.downloadAllImages();
        });
    }

    /**
     * 处理表单提交
     */
    handleSubmit() {
        const formData = new FormData(document.getElementById("characterForm"));
        
        const data = {
            appearance: formData.get("appearance") || "",
            age: formData.get("age") || null,
            gender: formData.get("gender") || null,
            style: formData.get("style") || "anime",
        };

        // 获取选中的表情
        const selectedExpressions = Array.from(
            document.querySelectorAll('input[name="expressions"]:checked')
        ).map(cb => cb.value);

        if (!data.appearance) {
            alert("请填写外观描述！");
            return;
        }

        // 生成 prompt
        const prompts = this.generator.generateAllPrompts(data, selectedExpressions);
        
        // 保存 prompts 和 data 供后续使用
        this.currentPrompts = prompts;
        this.currentData = data;
        
        // 显示结果
        this.displayPrompts(prompts);
        
        // 检查是否有 API Key，显示生成图片按钮
        const apiKey = document.getElementById("apiKey").value.trim();
        const generateBtn = document.getElementById("generateImagesBtn");
        if (apiKey) {
            generateBtn.style.display = "inline-flex";
        } else {
            generateBtn.style.display = "none";
        }
    }

    /**
     * 显示生成的 prompt
     */
    displayPrompts(prompts) {
        const container = document.getElementById("promptsContainer");
        const outputSection = document.getElementById("outputSection");
        
        container.innerHTML = "";

        // 按顺序显示：三视图在前，表情在后
        const viewKeys = ["front_view", "side_view", "back_view"];
        const expressionKeys = Object.keys(prompts).filter(k => k.startsWith("expression_"));

        // 显示三视图
        viewKeys.forEach(key => {
            if (prompts[key]) {
                container.appendChild(this.createPromptCard(prompts[key], key));
            }
        });

        // 显示表情
        expressionKeys.forEach(key => {
            container.appendChild(this.createPromptCard(prompts[key], key));
        });

        outputSection.style.display = "block";
        outputSection.scrollIntoView({ behavior: "smooth" });
    }

    /**
     * 创建 prompt 卡片
     */
    createPromptCard(promptData, key) {
        const card = document.createElement("div");
        card.className = "prompt-card";

        const header = document.createElement("div");
        header.className = "prompt-card-header";

        const title = document.createElement("h3");
        title.textContent = promptData.title;

        const copyBtn = document.createElement("button");
        copyBtn.className = "btn btn-small btn-copy";
        copyBtn.textContent = "复制";
        copyBtn.addEventListener("click", () => {
            this.copyToClipboard(promptData.prompt, copyBtn);
        });

        header.appendChild(title);
        header.appendChild(copyBtn);

        const content = document.createElement("div");
        content.className = "prompt-card-content";
        const textarea = document.createElement("textarea");
        textarea.value = promptData.prompt;
        textarea.readOnly = true;
        textarea.rows = Math.min(promptData.prompt.split("\n").length + 2, 15);
        content.appendChild(textarea);

        card.appendChild(header);
        card.appendChild(content);

        return card;
    }

    /**
     * 复制到剪贴板
     */
    async copyToClipboard(text, button) {
        try {
            await navigator.clipboard.writeText(text);
            
            // 显示成功反馈
            const originalText = button.textContent;
            button.textContent = "已复制！";
            button.classList.add("copied");
            
            setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove("copied");
            }, 2000);
        } catch (err) {
            console.error("复制失败:", err);
            alert("复制失败，请手动选择文本复制");
        }
    }

    /**
     * 复制所有 prompt
     */
    async copyAllPrompts() {
        const cards = document.querySelectorAll(".prompt-card");
        const allPrompts = [];

        cards.forEach(card => {
            const title = card.querySelector("h3").textContent;
            const prompt = card.querySelector("textarea").value;
            allPrompts.push(`=== ${title} ===\n${prompt}\n`);
        });

        const allText = allPrompts.join("\n\n");

        try {
            await navigator.clipboard.writeText(allText);
            
            const copyAllBtn = document.getElementById("copyAllBtn");
            const originalText = copyAllBtn.textContent;
            copyAllBtn.textContent = "已复制全部！";
            copyAllBtn.classList.add("copied");
            
            setTimeout(() => {
                copyAllBtn.textContent = originalText;
                copyAllBtn.classList.remove("copied");
            }, 2000);
        } catch (err) {
            console.error("复制失败:", err);
            alert("复制失败，请手动选择文本复制");
        }
    }

    /**
     * 清空表单
     */
    clearForm() {
        document.getElementById("characterForm").reset();
        this.setupExpressions(); // 重新设置表情复选框（默认全选）
        document.getElementById("outputSection").style.display = "none";
        document.getElementById("imagesSection").style.display = "none";
        this.currentPrompts = null;
        this.currentData = null;
    }

    /**
     * 生成图片（调用 Gemini API）
     */
    async generateImages() {
        const apiKey = document.getElementById("apiKey").value.trim();
        if (!apiKey) {
            alert("请先输入 Gemini API Key！");
            return;
        }

        if (!this.currentPrompts) {
            alert("请先生成 Prompt！");
            return;
        }

        const imagesSection = document.getElementById("imagesSection");
        const imagesContainer = document.getElementById("imagesContainer");
        const downloadAllBtn = document.getElementById("downloadAllBtn");
        const generateBtn = document.getElementById("generateImagesBtn");

        // 显示图片区域
        imagesSection.style.display = "block";
        imagesContainer.innerHTML = "<div class='loading'>正在生成图片，请稍候...</div>";
        generateBtn.disabled = true;
        generateBtn.textContent = "生成中...";

        const imageResults = {};
        const promptKeys = Object.keys(this.currentPrompts);

        try {
            // 逐个生成图片
            for (let i = 0; i < promptKeys.length; i++) {
                const key = promptKeys[i];
                const promptData = this.currentPrompts[key];
                
                // 显示进度
                imagesContainer.innerHTML = `
                    <div class='loading'>
                        <p>正在生成图片 ${i + 1}/${promptKeys.length}</p>
                        <p class='loading-detail'>${promptData.title}</p>
                        <div class='progress-bar'>
                            <div class='progress' style='width: ${((i + 1) / promptKeys.length) * 100}%'></div>
                        </div>
                    </div>
                `;

                try {
                    const imageUrl = await this.callGeminiAPI(apiKey, promptData.prompt);
                    imageResults[key] = {
                        title: promptData.title,
                        url: imageUrl,
                        prompt: promptData.prompt
                    };
                } catch (error) {
                    console.error(`生成 ${promptData.title} 失败:`, error);
                    imageResults[key] = {
                        title: promptData.title,
                        error: error.message,
                        prompt: promptData.prompt
                    };
                }

                // 添加延迟，避免 API 限流
                if (i < promptKeys.length - 1) {
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
            }

            // 显示生成的图片
            this.displayImages(imageResults);
            downloadAllBtn.style.display = "inline-flex";
            
        } catch (error) {
            console.error("生成图片失败:", error);
            imagesContainer.innerHTML = `
                <div class='error'>
                    <p>生成图片时出错：${error.message}</p>
                    <p>请检查 API Key 是否正确，或稍后重试。</p>
                </div>
            `;
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = "<span class='btn-icon'>🖼️</span> 生成图片";
            imagesSection.scrollIntoView({ behavior: "smooth" });
        }
    }

    /**
     * 调用 Gemini API 生成图片
     * 注意：由于 CORS 限制，可能需要通过后端代理
     */
    async callGeminiAPI(apiKey, prompt) {
        // 尝试多种 API 端点
        const apiEndpoints = [
            // Google AI Studio API (可能需要后端代理)
            `https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0:generateImages?key=${apiKey}`,
            // Vertex AI API (需要后端代理)
            // 其他可能的端点...
        ];

        const requestBody = {
            prompt: prompt,
            number_of_images: 1,
            aspect_ratio: "1:1",
            safety_filter_level: "block_some",
            person_generation: "allow_all"
        };

        // 尝试第一个端点
        const apiUrl = apiEndpoints[0];

        try {
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                const errorText = await response.text();
                let errorData;
                try {
                    errorData = JSON.parse(errorText);
                } catch {
                    errorData = { error: { message: errorText } };
                }
                
                // 检查是否是 CORS 错误
                if (response.status === 0 || errorText.includes("CORS")) {
                    throw new Error("CORS_ERROR");
                }
                
                throw new Error(errorData.error?.message || `API 错误: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            
            // 检查返回的数据结构
            if (data.generatedImages && data.generatedImages.length > 0) {
                const image = data.generatedImages[0];
                // 处理 base64 图片
                if (image.base64Image) {
                    return `data:image/png;base64,${image.base64Image}`;
                }
                return image.imageUrl || image.url;
            } else if (data.images && data.images.length > 0) {
                const image = data.images[0];
                if (image.base64Image) {
                    return `data:image/png;base64,${image.base64Image}`;
                }
                return image.url || image.imageUrl;
            } else {
                throw new Error("API 返回的数据格式不正确，请检查 API 文档");
            }
        } catch (error) {
            // 处理 CORS 错误
            if (error.message === "CORS_ERROR" || error.message.includes("CORS") || error.message.includes("NetworkError")) {
                throw new Error("CORS_ERROR: 由于浏览器安全限制，无法直接调用 API。\n\n解决方案：\n1. 使用后端代理服务器\n2. 使用 Google AI Studio 网页版\n3. 配置 CORS 代理");
            }
            throw error;
        }
    }

    /**
     * 显示生成的图片
     */
    displayImages(imageResults) {
        const container = document.getElementById("imagesContainer");
        container.innerHTML = "";

        const keys = Object.keys(imageResults);
        const viewKeys = ["front_view", "side_view", "back_view"];
        const expressionKeys = keys.filter(k => k.startsWith("expression_"));

        // 显示三视图
        viewKeys.forEach(key => {
            if (imageResults[key]) {
                container.appendChild(this.createImageCard(imageResults[key], key));
            }
        });

        // 显示表情
        expressionKeys.forEach(key => {
            if (imageResults[key]) {
                container.appendChild(this.createImageCard(imageResults[key], key));
            }
        });
    }

    /**
     * 创建图片卡片
     */
    createImageCard(imageData, key) {
        const card = document.createElement("div");
        card.className = "image-card";

        const header = document.createElement("div");
        header.className = "image-card-header";

        const title = document.createElement("h3");
        title.textContent = imageData.title;

        header.appendChild(title);

        const content = document.createElement("div");
        content.className = "image-card-content";

        if (imageData.error) {
            content.innerHTML = `
                <div class="error-message">
                    <p>❌ 生成失败</p>
                    <p>${imageData.error}</p>
                </div>
            `;
        } else if (imageData.url) {
            const img = document.createElement("img");
            img.src = imageData.url;
            img.alt = imageData.title;
            img.loading = "lazy";
            img.onerror = function() {
                this.parentElement.innerHTML = `
                    <div class="error-message">
                        <p>❌ 图片加载失败</p>
                    </div>
                `;
            };

            const downloadBtn = document.createElement("button");
            downloadBtn.className = "btn btn-small btn-download";
            downloadBtn.textContent = "下载";
            downloadBtn.addEventListener("click", () => {
                this.downloadImage(imageData.url, imageData.title);
            });

            content.appendChild(img);
            content.appendChild(downloadBtn);
        }

        card.appendChild(header);
        card.appendChild(content);

        return card;
    }

    /**
     * 下载单张图片
     */
    async downloadImage(imageUrl, filename) {
        try {
            const response = await fetch(imageUrl);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `${filename.replace(/[^a-zA-Z0-9]/g, "_")}.png`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error("下载图片失败:", error);
            alert("下载图片失败，请手动保存图片");
        }
    }

    /**
     * 下载所有图片
     */
    async downloadAllImages() {
        const images = document.querySelectorAll(".image-card img");
        if (images.length === 0) {
            alert("没有可下载的图片");
            return;
        }

        for (let i = 0; i < images.length; i++) {
            const img = images[i];
            const title = img.closest(".image-card").querySelector("h3").textContent;
            await this.downloadImage(img.src, title);
            // 添加延迟，避免浏览器阻止多个下载
            if (i < images.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 500));
            }
        }
    }
}

// 页面加载完成后初始化
document.addEventListener("DOMContentLoaded", () => {
    new PromptGeneratorUI();
});

