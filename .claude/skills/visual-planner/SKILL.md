# Visual Planner - 视觉规划技能

## 技能描述

视觉规划层核心技能，负责将文字结构翻译成视觉结构。输入是文章草稿、内容大纲、平台类型和风格要求，输出是标准化的图片 spec 列表。

此技能不是直接生成最终图片，而是为 image-card-builder 和 asset-sourcer 提供可执行的图像脚本。

## 快速开始

```bash
# 从母稿生成视觉方案
/visual-planner {topic-name} --input topics/{topic-name}/post.md

# 指定输出目录
/visual-planner {topic-name} --output topics/{topic-name}/fig/visual_plan.md

# 指定风格偏好
/visual-planner {topic-name} --style cute-tech --ratio 3:4
```

## 输入来源

默认按以下优先级读取：

1. `topics/{topic-name}/post.md` - 母稿（核心输入）
2. `topics/{topic-name}/outline.md` - 大纲
3. `01_定位与规则/` - 账号定位与平台规则
4. `04_知识卡片/` - 可复用的观点与表达
5. 用户补充的视觉偏好与参考案例

## 输出文件

在 `topics/{topic-name}/fig/` 下生成并维护单一文件：

**`visual_plan.md`** - 视觉规划与执行全案

包含以下章节：

1. 视觉策略总览
2. 素材获取状态（迭代区）
3. 补充素材清单（如需要）
4. 图片执行脚本（精修版）
5. 执行日志 - post-builder 填写
6. 审核意见 - visual-post-reviewer 填写

## 工作流程

```
读取母稿 -> 提炼主题 -> 定义视觉叙事 -> 输出 spec -> 迭代素材需求
    ↓
素材获取完成 -> 评估素材足够 -> 输出详细执行方案 -> 交接 builder
```

## 输出格式

### 一、视觉策略总览结构

```markdown
# {选题名称} - 视觉规划与执行全案

## 一、视觉策略总览

### 主题摘要
- 核心主题：
- 核心立场：
- 封面抓手：
- 视觉语气：
- 关键词：

### 视觉总原则
- 调性：
- 主色：
- 辅色：
- 禁止风格：
- 统一性要求：
```

### 二、素材获取状态结构

```markdown
## 二、素材获取状态（第 N 轮）

| 序号 | 素材名称 | 用途 | 获取方式 | 文件路径 | 质量评分 | 状态 | 说明 |
|------|----------|------|----------|----------|----------|------|------|
| 1 | OpenClaw Logo | 封面主视觉 | material-fetcher | fig/素材/logo_openclaw.svg | 90 | ✅ 已获取 | SVG 格式 |

### 补充素材清单（第 N 轮）

| 序号 | 素材名称 | 用途 | 建议搜索关键词 | 建议来源 | 优先级 | 负责方 |
|------|----------|------|---------------|----------|--------|--------|
| 1 | XXX | XXX | XXX | XXX | P0 | 人工 |
```

### 三、图片执行脚本结构

```markdown
## 三、图片执行脚本

| id | 用途 | information_role | theme_anchor | text_binding | 获取方式 | 状态 |
|----|------|------------------|-------------|-------------|----------|------|
| 01 | 封面 | cover | XXX | XXX | hybrid-edit | 待执行 |

### 01_cover
- purpose: 封面
- theme_anchor: 主题锚点
- text_binding: 对应正文段落
- visual_goal: 这张图希望读者感受到什么
- failure_mode: 哪些做法会导致跑题、廉价或空泛
- source_route: 素材获取路线
- builder_freedom: builder 可自由发挥的程度
- must_have: 必须包含的元素
- must_avoid: 必须避免的问题
- execution_instruction: 执行指令
- prompt / keywords: AI 生图提示词（如需）
- ratio: 图片比例
```

## Spec 设计

每张图片的 spec 至少应包含：

```json
{
  "id": "cover-01",
  "purpose": "封面",
  "template": "cover-alert",
  "render_mode": "direct",
  "aspect_ratio": "3:4",
  "title": "致命 RCE 漏洞",
  "subtitle": "OpenClaw 爆出高危问题",
  "body": [
    "一个恶意链接，可能直接接管电脑",
    "别把高权限 Agent 默认运行当小事"
  ],
  "highlights": ["RCE", "高危", "默认高权限"],
  "visual_tone": "高危警示、科技感、适合小红书封面",
  "must_include": ["警示 icon", "大标题", "中央视觉元素"],
  "must_avoid": ["信息过密", "背景过花", "低质黑客素材"],
  "asset_needs": [],
  "notes_for_builder": "整体留白充足，标题要强，正文不超过三行"
}
```

## 图片数量规则

- 默认总数 3–5 张
- 没有强理由，不要超过 5 张
- 每张图都必须有存在理由
- 不允许"为了凑数"加图

## information_role 类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| `cover` | 封面图 | 抓住注意力，建立主题 |
| `evidence` | 证据图 | 展示数据、截图、事实 |
| `concept` | 概念图 | 解释抽象概念 |
| `scene` | 场景图 | 建立使用场景感 |
| `quote` | 引用图 | 强化金句传播 |
| `transition` | 转场图 | 段落间过渡 |
| `summary` | 总结图 | 收束全文观点 |

## render_mode 类型

| 类型 | 说明 | 执行路线 |
|------|------|----------|
| `direct` | 直接绘制 | 交 image-card-builder 直接渲染 |
| `sourced` | 需要素材 | 先交 asset-sourcer 获取素材 |
| `hybrid` | 素材 + 绘制 | 素材获取后交 builder 合成 |

## 模板类型建议

优先支持的模板：

| 模板 | 用途 | 风格 |
|------|------|------|
| `cover-alert` | 高危漏洞、翻车、紧急提醒 | 警示风 |
| `cover-minimal` | 大标题 + 正文的极简信息卡 | 极简风 |
| `cover-list` | 三点总结、五个结论、步骤式 | 清单风 |
| `quote-card` | 引用卡片、金句图 | 文字主导 |
| `compare-card` | 对比、优缺点、前后变化 | 对比风 |
| `timeline-card` | 时间线、发展脉络 | 流程风 |

## AI Prompt 规则

所有 `ai-generate` 或 `hybrid-edit` 项必须输出高质量 prompt。

prompt 至少包含：
- 主体与场景
- 主题意图
- 风格参考
- 构图方式
- 色彩控制
- 光线与质感
- 画面应避免的元素
- 比例要求
- 需要预留文字区时必须说明

### Prompt 模板

```markdown
**Prompt**:
主体：[描述画面中心的主体元素]
场景：[描述背景和环境]
风格：[cute, tech, minimalist, balanced, premium 等关键词]
构图：[居中、三分法、对称、留白位置等]
色彩：[使用自然语言描述，如 deep black background, tech blue highlight]
光线：[柔和、强烈、侧光、逆光等]
质感：[光滑、磨砂、金属、玻璃等]
避免：[画面中不应出现的元素]
比例：[3:4, 16:9, 1:1 等]
```

## 与其他技能协作

| 技能 | 协作内容 |
|------|----------|
| `xhs-adapter` | 接收平台适配需求，决定图片数量和作用 |
| `asset-sourcer` | 获取外部素材（背景图、截图、logo 等） |
| `image-card-builder` | 渲染 spec 成图像 |
| `visual-reviewer` | 审核视觉方案是否成立 |
| `material-fetcher` | 获取品牌资产、Logo 等素材 |

## 使用示例

### 示例 1：从小红书母稿生成视觉方案

```bash
/visual-planner openclaw-analysis --input topics/openclaw-analysis/post.md
```

### 示例 2：指定风格偏好

```bash
/visual-planner ai-tools --style cute-tech --ratio 3:4
```

### 示例 3：预览模式（仅查看 spec，不生成文件）

```bash
/visual-planner test-topic --dry-run
```

## 高质量视觉规划标准

规划的视觉方案必须满足：

1. 紧扣主题
2. 有传播感，但不低俗
3. 有完成度，不像临时素材
4. 有平台感，适配小红书/头条/公众号
5. 能被 builder 做成高级成片
6. 每张图都有明确的信息任务
7. 整套图在风格、叙事、色调上统一

## 必须避免的问题

- 空泛科技图
- 套模板式蓝色 AI 图
- 与正文无关的"宇宙脑图""机器人发光图"
- 只好看但没有信息任务的图
- 与平台用户气质不匹配的图片
- 不能落地的复杂设计
- 素材需求不清导致无法执行
- 在素材不足时强行输出执行方案

## 迭代机制

```
评估素材 → 不足则输出补充清单 → material-fetcher/人工补充 → 重新评估 → 循环直到足够
```

**素材足够的标准**：
- 核心素材（Logo、关键截图）质量分≥80
- 每张图都有对应的素材支撑
- 无关键素材缺失

## 文件命名规范

输出的 visual_plan.md 统一放在：

```
topics/{topic-name}/fig/visual_plan.md
```

中间素材和定稿图也放在同一 fig 目录下：

```
topics/{topic-name}/fig/
├── visual_plan.md        # 视觉规划与执行全案
├── 素材/                 # 原始素材
├── 定稿图/               # 最终输出
└── build-log.md          # 执行日志
```

## 环境要求

- Python 3.8+（如使用 Python 实现）
- Node.js 16+（如使用 Node.js 实现）
- 访问 topics/目录的读写权限

## 最佳实践

1. **先读母稿** - 理解文章核心观点和情绪基调
2. **提炼主题** - 用一句话说清这篇文章要表达什么
3. **定义叙事** - 规划封面抓什么、中间怎么展开、如何收尾
4. **明确素材** - 哪些图可以直接画，哪些需要外部素材
5. **写清 spec** - 让 builder 不需要做语义猜测
6. **等待素材** - 素材不足时不要强行输出执行方案
7. **迭代优化** - 根据 reviewer 意见调整视觉方案
