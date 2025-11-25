# 剧本到分镜生成详细流程图

## 完整系统流程图（ASCII艺术版）

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          用户输入阶段                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  用户在Web界面输入剧本文本      │
                    │  - 剧本标题（可选）            │
                    │  - 剧本文本内容                │
                    │  - 选择：优先使用资源库资源     │
                    └───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  前端验证与处理                 │
                    │  ✓ 检查输入非空                │
                    │  ✓ 显示加载状态                │
                    │  ✓ 准备API请求                 │
                    └───────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        API请求阶段                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        POST /api/storyboard/generate        POST /api/script/parse
        {                                   {
          "script_text": "...",               "script_text": "...",
          "title": "...",                     "title": "..."
          "prefer_existing_resources": true   }
        }
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       服务器接收阶段                                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌───────────────────────┐      ┌───────────────────────┐
        │  有script_text?       │      │  有script_data?      │
        └───────────────────────┘      └───────────────────────┘
                    │                               │
            YES     │                               │     YES
                    ▼                               ▼
        ┌───────────────────────┐      ┌───────────────────────┐
        │  调用ScriptParser      │      │  直接使用结构化数据    │
        │  .parse()              │      │                        │
        └───────────────────────┘      └───────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       剧本解析阶段 (ScriptParser)                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌───────────────────────┐      ┌───────────────────────┐
        │  提取标题              │      │  解析场景列表          │
        │  _extract_title()      │      │  _parse_scenes()       │
        │                        │      │                        │
        │  检查前5行             │      │  识别场景标记：        │
        │  查找非空行            │      │  - "场景1"            │
        │  排除场景标记          │      │  - "第1场"            │
        │                        │      │  - "【场景1】"        │
        └───────────────────────┘      └───────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  解析场景内容                  │
                    │  _parse_scene_line()           │
                    │                                │
                    │  ├─ 解析地点                   │
                    │  │   "地点: XXX"               │
                    │  │                             │
                    │  ├─ 解析时间                   │
                    │  │   "时间: XXX"               │
                    │  │                             │
                    │  ├─ 解析对话                   │
                    │  │   "角色名: 对话内容"        │
                    │  │   "角色名: 对话（情绪）"    │
                    │  │                             │
                    │  ├─ 解析动作                   │
                    │  │   "动作: XXX"              │
                    │  │   "[动作] XXX"             │
                    │  │                             │
                    │  └─ 解析备注                   │
                    │     "备注: XXX"                │
                    └───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  提取角色信息                  │
                    │  _extract_characters()         │
                    │                                │
                    │  从场景对话中提取角色名        │
                    │  创建角色信息字典               │
                    └───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  生成结构化剧本数据             │
                    │  {                             │
                    │    "title": "...",             │
                    │    "scenes": [...],            │
                    │    "characters": {...}         │
                    │  }                             │
                    └───────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       资源匹配阶段 (ResourceMatcher)                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌───────────────────────┐      ┌───────────────────────┐
        │  prefer_existing_     │      │  跳过资源匹配         │
        │  resources = true?     │      │  直接生成分镜         │
        └───────────────────────┘      └───────────────────────┘
                    │
            YES     │
                    ▼
        ┌───────────────────────────────────────────────────┐
        │  并行匹配各类资源                                   │
        └───────────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┬───────────┬───────────┐
        │           │           │           │           │
        ▼           ▼           ▼           ▼           ▼
┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│ 匹配角色   │ │ 匹配场景   │ │ 匹配道具   │ │ 匹配动作   │
│           │ │           │ │           │ │           │
│ 1.搜索    │ │ 1.搜索    │ │ 1.搜索    │ │ 1.搜索    │
│ 2.名称    │ │ 2.类型    │ │ 2.名称    │ │ 2.类型    │
│ 3.描述    │ │ 3.氛围    │ │ 3.类别    │ │ 3.名称    │
│ 4.标签    │ │ 4.风格    │ │ 4.描述    │ │           │
│ 5.风格    │ │ 5.时间    │ │           │ │           │
│ 6.计算    │ │ 6.天气    │ │           │ │           │
│   分数    │ │ 7.计算    │ │           │ │           │
│           │ │   分数    │ │           │ │           │
└───────────┘ └───────────┘ └───────────┘ └───────────┘
        │           │           │           │
        └───────────┴───────────┴───────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │  创建资源引用                  │
        │  ResourceReference            │
        │  {                            │
        │    resource_id,               │
        │    resource_type,             │
        │    resource_name,             │
        │    match_score,              │
        │    match_reason               │
        │  }                            │
        └───────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       分镜生成阶段 (StoryboardGenerator)                  │
└─────────────────────────────────────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │  遍历场景列表                  │
        │  for scene in scenes:         │
        └───────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │  为每个场景生成镜头            │
        │  _generate_scene_shots()      │
        └───────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐      ┌───────────────┐
│ 匹配场景资源   │      │ 匹配角色资源   │
│               │      │               │
│ match_scene() │      │ match_        │
│               │      │ character()   │
└───────────────┘      └───────────────┘
        │                       │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │  处理对话                      │
        │  for dialogue in dialogues:    │
        │    ├─ 确定镜头类型             │
        │    │   _determine_shot_type_  │
        │    │      for_dialogue()       │
        │    │                           │
        │    ├─ 构建画面描述             │
        │    │   _build_shot_           │
        │    │      description()        │
        │    │                           │
        │    └─ 创建Shot对象             │
        └───────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │  处理动作                      │
        │  if action:                   │
        │    ├─ 确定镜头类型             │
        │    ├─ 构建画面描述             │
        │    └─ 创建Shot对象             │
        └───────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │  添加资源引用到Shot            │
        │  shot.character_resources      │
        │  shot.scene_resource           │
        │  shot.prop_resources           │
        │  shot.action_resources         │
        └───────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │  创建Storyboard对象            │
        │  {                            │
        │    title,                     │
        │    shots: [Shot1, Shot2, ...],│
        │    metadata: {                │
        │      total_duration,          │
        │      total_shots,             │
        │      source,                  │
        │      prefer_existing_        │
        │        resources              │
        │    }                          │
        │  }                            │
        └───────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │  转换为字典格式                │
        │  storyboard.to_dict()         │
        └───────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       响应返回阶段                                        │
└─────────────────────────────────────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────┐
        │  返回JSON响应                  │
        │  {                            │
        │    "success": true,           │
        │    "data": {...},             │
        │    "message": "..."           │
        │  }                            │
        └───────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       前端展示阶段                                        │
└─────────────────────────────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐      ┌───────────────┐
│ 显示资源匹配   │      │ 显示分镜脚本   │
│               │      │               │
│ - 场景资源    │      │ - 统计信息    │
│ - 角色资源    │      │ - 镜头列表    │
│ - 道具资源    │      │ - 资源标注    │
│ - 动作资源    │      │ - 导出功能    │
│ - 匹配分数    │      │               │
└───────────────┘      └───────────────┘
```

## 详细步骤说明

### 步骤1: 用户输入 (Web界面)

```
用户操作:
├─ 在文本框中输入剧本文本
├─ （可选）输入剧本标题
├─ （可选）勾选"优先使用资源库资源"
└─ 点击"生成分镜脚本"按钮

前端处理:
├─ 验证输入非空
├─ 显示加载状态和进度条
└─ 发送POST请求到 /api/storyboard/generate
```

### 步骤2: 服务器接收请求

```python
# Flask路由处理
@app.route("/api/storyboard/generate", methods=["POST"])
def generate_storyboard():
    # 1. 获取请求数据
    data = request.get_json()
    script_text = data.get("script_text")
    prefer_resources = data.get("prefer_existing_resources", True)
    
    # 2. 解析剧本（如果有script_text）
    if script_text:
        script_data = script_parser.parse(script_text, title)
    
    # 3. 生成分镜
    storyboard = storyboard_generator.generate_from_script(
        script_data,
        prefer_existing_resources=prefer_resources
    )
    
    # 4. 返回结果
    return jsonify({
        "success": True,
        "data": storyboard.to_dict()
    })
```

### 步骤3: 剧本解析 (ScriptParser)

```python
# 解析流程
def parse(script_text, title):
    lines = script_text.split('\n')
    
    # 3.1 提取标题
    if not title:
        title = _extract_title(lines)  # 检查前5行
    
    # 3.2 解析场景
    scenes = _parse_scenes(lines)
    #    ├─ 识别场景标记（场景1、第1场等）
    #    ├─ 解析每个场景的内容
    #    │   ├─ 地点: location
    #    │   ├─ 时间: time
    #    │   ├─ 对话: dialogue[]
    #    │   ├─ 动作: action
    #    │   └─ 备注: notes
    #    └─ 提取角色列表
    
    # 3.3 提取角色信息
    characters = _extract_characters(scenes)
    
    return {
        "title": title,
        "scenes": scenes,
        "characters": characters
    }
```

### 步骤4: 资源匹配 (ResourceMatcher)

```python
# 如果启用资源匹配
if prefer_existing_resources:
    # 4.1 匹配角色
    for char_name in scene.characters:
        match = matcher.match_character(
            name=char_name,
            description=char_info.get("description"),
            style=scene_style
        )
        # 计算匹配分数:
        #   名称相似度 × 0.4
        #   + 描述相似度 × 0.3
        #   + 标签匹配度 × 0.2
        #   + 风格匹配 × 0.1
        #   = 总分 (0-1)
    
    # 4.2 匹配场景
    match = matcher.match_scene(
        location_type=extract_location_type(location),
        description=location,
        mood=notes,
        time_of_day=time
    )
    # 计算匹配分数:
    #   场景类型匹配 × 0.25
    #   + 氛围匹配 × 0.25
    #   + 风格匹配 × 0.20
    #   + 时间匹配 × 0.15
    #   + 天气匹配 × 0.15
    #   + 描述相似度 × 0.30
    
    # 4.3 匹配道具和动作（类似流程）
```

### 步骤5: 分镜生成 (StoryboardGenerator)

```python
# 为每个场景生成镜头
def _generate_scene_shots(scene_data, ...):
    shots = []
    
    # 5.1 匹配场景和角色资源
    scene_resource = match_scene(...)
    character_resources = {}
    for char in characters:
        char_resource = match_character(...)
        if char_resource:
            character_resources[char] = char_resource[1]
    
    # 5.2 处理对话
    for dialogue in scene.dialogue:
        # 确定镜头类型
        shot_type = _determine_shot_type_for_dialogue(
            dialogue.text,
            dialogue.emotion
        )
        
        # 构建画面描述（包含资源标注）
        description = _build_shot_description(
            location=location,
            characters=[dialogue.character],
            dialogue=dialogue.text,
            scene_resource=scene_resource,
            character_resources=character_resources
        )
        # 描述格式:
        # "场景: XXX（来自资源库） | 
        #  角色: YYY（来自资源库） | 
        #  对话: ZZZ"
        
        # 创建Shot对象
        shot = Shot(
            shot_number=shot_number,
            scene_number=scene_number,
            shot_type=shot_type,
            duration=3.0,
            description=description,
            characters=[dialogue.character],
            dialogue=dialogue.text,
            character_resources=[character_resources.get(...)],
            scene_resource=scene_resource
        )
        shots.append(shot)
    
    # 5.3 处理动作（如果没有对话）
    if not dialogue and action:
        shot = create_action_shot(...)
        shots.append(shot)
    
    return shots
```

### 步骤6: 结果组装

```python
# 创建Storyboard对象
storyboard = Storyboard(
    title=title,
    shots=all_shots,
    metadata={
        "source": "script",
        "prefer_existing_resources": prefer_resources
    }
)

# 自动计算统计信息
# - total_duration: sum(shot.duration)
# - total_shots: len(shots)

# 转换为字典
storyboard_dict = storyboard.to_dict()
```

### 步骤7: 前端展示

```javascript
// 接收响应
const result = await response.json();
const storyboard = result.data;

// 7.1 显示统计信息
displayStats({
    total_shots: storyboard.metadata.total_shots,
    total_duration: storyboard.metadata.total_duration,
    title: storyboard.title
});

// 7.2 显示资源匹配结果
if (prefer_resources) {
    displayResources(storyboard.storyboard);
    // 显示匹配到的:
    // - 场景资源
    // - 角色资源
    // - 道具资源
    // - 动作资源
    // - 匹配分数和原因
}

// 7.3 显示分镜镜头列表
displayShots(storyboard.storyboard);
// 每个镜头显示:
// - 镜头编号和场景编号
// - 镜头类型和时长
// - 画面描述（包含资源标注）
// - 对话内容
// - 使用的资源列表
```

## 关键数据转换

```
输入: 纯文本剧本
  ↓ ScriptParser.parse()
结构化剧本数据 (JSON)
  ↓ ResourceMatcher.match_*()
资源引用列表 (ResourceReference[])
  ↓ StoryboardGenerator.generate_from_script()
分镜脚本对象 (Storyboard)
  ↓ Storyboard.to_dict()
分镜脚本字典 (Dict)
  ↓ JSON序列化
JSON响应
  ↓ 前端解析
前端展示 (HTML)
```

## 资源匹配详细算法

### 角色匹配算法

```
输入: 角色名称、描述、风格、标签
  ↓
1. 搜索资源库
   search_resources(keyword=name, tags=tags, type=CHARACTER)
  ↓
2. 风格过滤
   if style: filter by style
  ↓
3. 计算匹配分数
   for each character:
     score = 0
     if name:
       name_score = similarity(name, char.name)
       score += name_score × 0.4
     if description:
       desc_score = text_similarity(description, char.description)
       score += desc_score × 0.3
     if tags:
       tag_score = tag_match(tags, char.tags)
       score += tag_score × 0.2
     if style == char.style:
       score += 0.1
  ↓
4. 选择最佳匹配
   if max(score) >= min_score(0.3):
     return (character, ResourceReference)
   else:
     return None
```

### 场景匹配算法

```
输入: 地点类型、描述、氛围、时间、天气
  ↓
1. 搜索资源库
   search_resources(keyword=description, type=SCENE)
  ↓
2. 计算匹配分数
   for each scene:
     score = 0
     if location_type == scene.location_type:
       score += 0.25
     if mood == scene.mood:
       score += 0.25
     if style == scene.style:
       score += 0.20
     if time_of_day == scene.time_of_day:
       score += 0.15
     if weather == scene.weather:
       score += 0.15
     if description:
       desc_score = text_similarity(description, scene.description)
       score += desc_score × 0.30
  ↓
3. 选择最佳匹配
   if max(score) >= min_score(0.3):
     return (scene, ResourceReference)
   else:
     return None
```

## 镜头类型确定逻辑

```
对话镜头类型确定:
  ↓
if emotion in ["悲伤", "愤怒", "惊讶", "恐惧"]:
  return CLOSE_UP  // 情绪强烈用特写
  ↓
if len(dialogue) < 20:
  return CLOSE_UP  // 短对话用特写
  ↓
return MEDIUM  // 默认中景

动作镜头类型确定:
  ↓
if action contains "跑" or "跳":
  return WIDE  // 大动作用全景
  ↓
if action contains "看" or "观察":
  return CLOSE_UP  // 观察用特写
  ↓
return MEDIUM  // 默认中景
```

## 错误处理流程

```
错误类型 → 处理方式
─────────────────────────────────────────
输入为空 → 返回400错误，提示用户
解析失败 → 使用默认场景，继续处理
资源匹配失败 → 跳过匹配，使用原始描述
生成异常 → 返回500错误，包含错误信息
网络错误 → 前端显示错误提示
```

## 性能指标

- **剧本解析**: < 1秒（1000行剧本）
- **资源匹配**: < 2秒（100个资源）
- **分镜生成**: < 3秒（10个场景，50个镜头）
- **总响应时间**: < 5秒（典型场景）

## 扩展点

1. **AI增强**: 使用LLM优化解析和匹配
2. **缓存**: 缓存资源列表和匹配结果
3. **并行处理**: 场景处理并行化
4. **增量生成**: 支持修改已有镜头

