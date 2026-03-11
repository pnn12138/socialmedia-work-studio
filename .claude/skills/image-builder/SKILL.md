# Image Builder - 图像生成流程编排技能

## 技能描述

整合视觉规划、素材检索、图像合成、导出质检的端到端图像生成流程编排技能。

根据 visual-planner 输出的视觉方案，自动调度各图像 처리 技能，批量生成定稿图。

## 快速开始

```bash
# 执行完整流程
/image-builder {topic-name} --plan topics/{topic-name}/fig/visual_plan.md

# 预览模式（不执行，仅查看计划）
/image-builder {topic-name} --plan topics/{topic-name}/fig/visual_plan.md --dry-run

# 指定输出目录
/image-builder {topic-name} --plan visual_plan.md --output-dir /path/to/output
```

## 使用方式

### 基础用法

```bash
# 处理单个选题
/image-builder openclaw-analysis --plan topics/openclaw-analysis/fig/visual_plan.md

# 批量处理（shell 脚本）
for topic in topics/*/; do
    topic_name=$(basename "$topic")
    image-builder "$topic_name" --plan "topics/$topic_name/fig/visual_plan.md"
done
```

### 工作流程

```
1. 读取 visual_plan.md 中的图片执行脚本
   ↓
2. 解析每张图片的 source_mode 和 post_process_plan
   ↓
3. 根据 source_mode 选择执行路径：
   ├── existing: 直接使用素材
   ├── hybrid-edit: 智能裁剪 + 后处理
   ├── quote-card: 创建引用卡片
   ├── comparison: 创建对比图
   └── ai-generate: 提示用户外部生成
   ↓
4. 输出定稿图到 fig/定稿图/
   ↓
5. 保存执行日志到 build-log.json
```

## 输入参数

| 参数 | 说明 | 必需 |
|------|------|------|
| `topic` | 选题名称 | 是 |
| `--plan` | 视觉规划文件路径 | 是 |
| `--output-dir` | 输出目录（可选） | 否 |
| `--dry-run` | 仅预览，不执行 | 否 |

## visual_plan.md 格式要求

```markdown
# {选题名称} - 视觉规划与执行全案

## 三、图片执行脚本

### 01_cover
- id: 01_cover
- purpose: 封面
- source_mode: hybrid-edit
- source_file: fig/素材/logo_openclaw.svg
- ratio: 3:4
- output_width: 1080
- output_height: 1440
- post_process_plan:
  - type: text
    content: "标题文字"
    position: {anchor: "top-center"}
    size: 48
    color: "#FFFFFF"

### 02_quote
- id: 02_quote
- purpose: 引用卡片
- source_mode: quote-card
- quote: "这是一句引用"
- author: "作者名"
- style: tech-dark
- output_size: [1080, 1080]
```

## source_mode 支持类型

| 类型 | 说明 | 必需字段 |
|------|------|----------|
| `existing` | 直接使用现有素材 | `source_file` |
| `hybrid-edit` | 智能裁剪 + 后处理 | `source_file`, `ratio`, `post_process_plan` |
| `quote-card` | 创建引用卡片 | `quote`, `author`, `style` |
| `comparison` | 创建对比图 | `image1`, `image2`, `labels` |
| `ai-generate` / `external-ai` | AI 生成（需外部调用） | `prompt` |

## 输出

```
topics/{topic-name}/fig/
├── 定稿图/
│   ├── 01_cover.png          # 封面定稿
│   ├── 02_quote.png          # 引用卡片
│   ├── 03_comparison.png     # 对比图
│   └── ...
├── 原始素材/
│   └── ...                   # 中间素材
└── build-log.json            # 执行日志
```

## 执行日志格式

```json
[
  {
    "timestamp": "2026-03-10T12:00:00",
    "level": "info",
    "message": "Starting image build for topic: openclaw-analysis"
  },
  {
    "timestamp": "2026-03-10T12:00:01",
    "level": "info",
    "message": "Processing 01_cover: 封面"
  },
  {
    "timestamp": "2026-03-10T12:00:02",
    "level": "info",
    "message": "Downloaded: https://... -> topics/openclaw-analysis/fig/原始素材/bg.jpg"
  }
]
```

## 环境要求

- Python 3.8+
- Pillow
- OpenCV
- Requests

## 安装依赖

```bash
pip install pillow opencv-python requests
```

## 与其他技能协作

| 技能 | 协作内容 |
|------|----------|
| `visual-planner` | 读取 visual_plan.md 中的执行方案 |
| `image-compose-local` | 执行图像后处理（加字、调色、拼接） |
| `smart-cropper` | 智能裁剪（人脸检测、显著区域） |
| `background-remover` | 去背景处理 |
| `cover-layout-maker` | 封面排版 |
| `image-export-qc` | 导出质检 |
| `material-fetcher` | 获取素材 |

## 错误处理

| 错误 | 处理方式 |
|------|----------|
| 素材文件不存在 | 记录错误，跳过该图片，继续处理下一张 |
| visual_plan.md 格式错误 | 尝试解析，失败则报错退出 |
| 后处理操作失败 | 记录错误，尝试回退方案 |
| AI 生成请求 | 记录 prompt，提示用户外部生成 |

## 使用示例

### 示例 1：完整的封面生成

```bash
# visual_plan.md 内容：
# ### 01_cover
# - id: 01_cover
# - purpose: 封面
# - source_mode: hybrid-edit
# - source_file: fig/素材/bg.jpg
# - ratio: 3:4
# - post_process_plan:
#   - type: text
#     content: "AI 安全工具 OpenClaw"
#     size: 48
#     color: "#FFFFFF"

/image-builder openclaw-analysis --plan topics/openclaw-analysis/fig/visual_plan.md
```

### 示例 2：引用卡片批量生成

```bash
# visual_plan.md 内容：
# ### 02_quote_01
# - id: 02_quote_01
# - source_mode: quote-card
# - quote: "第一句引用"
# - style: tech-dark
#
# ### 03_quote_02
# - id: 03_quote_02
# - source_mode: quote-card
# - quote: "第二句引用"
# - style: minimalist

/image-builder quotes-topic --plan topics/quotes-topic/fig/visual_plan.md
```

### 示例 3：预览模式

```bash
# 查看将要执行的操作，不实际处理
/image-builder test-topic --plan topics/test-topic/fig/visual_plan.md --dry-run
```

## 平台尺寸规范

| 平台 | 类型 | 推荐尺寸 |
|------|------|----------|
| 小红书 | 封面 | 1080x1440 (3:4) |
| 小红书 | 内页 | 1080x1080 (1:1) |
| 今日头条 | 封面 | 1280x720 (16:9) |
| 微信公众号 | 封面 | 900x383 (2.35:1) |

## 最佳实践

1. **先执行 material-fetcher 获取素材**
2. **确保 visual_plan.md 格式正确**
3. **使用 dry-run 预览计划**
4. **检查 build-log.json 了解执行详情**
5. **失败时查看错误日志，补充缺失素材**
