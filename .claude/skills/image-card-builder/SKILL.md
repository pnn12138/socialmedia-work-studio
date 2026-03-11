# Image Card Builder - 图像卡片构建技能

## 技能描述

图像生成层核心技能，负责将 visual-planner 输出的 spec 渲染成图像。优先支持"文本主导型图片"，如白底黑字信息卡、漏洞警示封面、三点总结图、观点图、对比图、时间线图。

此技能采用模板系统，而不是每次从零生成。底层实现优先采用 HTML/CSS + Playwright 截图。

## 快速开始

```bash
# 从 visual_plan.md 执行图像生成
/image-card-builder {topic-name} --plan topics/{topic-name}/fig/visual_plan.md

# 处理单张 spec
/image-card-builder --spec fig/specs/01_cover.json

# 预览模式（不执行，仅查看计划）
/image-card-builder {topic-name} --plan visual_plan.md --dry-run

# 指定模板
/image-card-builder --spec 01_cover.json --template cover-alert
```

## 输入来源

默认按以下优先级读取：

1. `topics/{topic-name}/fig/visual_plan.md` - 视觉规划与执行全案（核心输入）
2. `topics/{topic-name}/fig/specs/*.json` - 单张 spec 文件
3. `topics/{topic-name}/fig/素材/` - 原始素材
4. 用户补充的风格偏好与参考案例

## 输出文件

在 `topics/{topic-name}/fig/` 下生成：

```
topics/{topic-name}/fig/
├── output/            # 最终输出
│   ├── 01_cover.png
│   ├── 02_inner_01.png
│   └── ...
├── intermediate/      # 中间文件（HTML/SVG）
│   ├── 01_cover.html
│   └── ...
├── specs/             # spec 备份
│   ├── 01_cover.json
│   └── ...
└── build-log.md       # 执行日志
```

## 模板系统

### 优先支持的模板

| 模板 | 用途 | 风格 | 适用场景 |
|------|------|------|----------|
| `cover-alert` | 高危漏洞、翻车、紧急提醒 | 警示风 | 安全警示、风险提示 |
| `cover-minimal` | 大标题 + 正文的极简信息卡 | 极简风 | 观点表达、金句图 |
| `cover-list` | 三点总结、五个结论、步骤式 | 清单风 | 工具清单、步骤说明 |
| `quote-card` | 引用卡片、金句图 | 文字主导 | 名人名言、核心观点 |
| `compare-card` | 对比、优缺点、前后变化 | 对比风 | 前后对比、优缺点分析 |
| `timeline-card` | 时间线、发展脉络 | 流程风 | 事件发展、历史演进 |

### 模板变量系统

每个模板应支持以下统一变量：

```json
{
  "theme": {
    "font": "系统字体栈",
    "primaryColor": "主色",
    "accentColor": "强调色",
    "backgroundColor": "背景色",
    "borderRadius": "圆角大小",
    "shadow": "阴影配置",
    "padding": "边距",
    "titleFontSize": "标题字号",
    "bodyFontSize": "正文字号",
    "lineHeight": "行高"
  }
}
```

## 输入参数

### 命令行参数

```bash
# 必需参数
--plan              # visual_plan.md 文件路径
--spec              # 单张 spec 文件路径
--template          # 指定模板（可选）
--output-dir        # 输出目录（可选）
--dry-run           # 仅预览，不执行
--theme             # 主题风格（cute-tech/minimalist/tech-dark）
```

### Spec 字段要求

```json
{
  "id": "cover-01",
  "purpose": "封面",
  "template": "cover-alert",
  "render_mode": "direct",
  "aspect_ratio": "3:4",
  "title": "致命 RCE 漏洞",
  "subtitle": "OpenClaw 爆出高危问题",
  "body": ["要点 1", "要点 2"],
  "highlights": ["RCE", "高危"],
  "visual_tone": "高危警示、科技感",
  "must_include": ["警示 icon", "大标题"],
  "must_avoid": ["信息过密", "背景过花"],
  "asset_needs": [],
  "notes_for_builder": "整体留白充足"
}
```

## 工作流程

```
读取 visual_plan.md -> 解析 spec -> 选择模板 -> 渲染 HTML/CSS -> Playwright 截图 -> 输出 PNG
                                              ↓
                                        保存中间文件
                                              ↓
                                        记录执行日志
```

## 底层技术路线

### 最推荐：HTML/CSS + Playwright 截图

**优点**：
- 易于调试
- 适合中文排版
- 多模板可复用
- 方便后续做主题系统
- 适合 3:4 小红书竖版图

**实现方式**：
```javascript
// 1. 根据 spec 生成 HTML
const html = generateHTML(spec, template);

// 2. 用 Playwright 打开并截图
const browser = await playwright.chromium.launch();
const page = await browser.newPage();
await page.setContent(html);
await page.screenshot({ path: outputPath });
```

### 第二推荐：SVG + resvg-js

**适用场景**：
- 扁平化程度更高的模板
- 矢量感更强的设计
- 流程图、结构性较强的封面

### 第三推荐：node-canvas

**适用场景**：
- 不依赖浏览器环境的 Node 脚本
- 固定模板批量生成
- 简单贴图、文本卡片

## render_mode 处理

| render_mode | 说明 | 处理路线 |
|-------------|------|----------|
| `direct` | 直接绘制 | 直接用模板渲染 |
| `sourced` | 需要素材 | 先等 asset-sourcer 获取素材 |
| `hybrid` | 素材 + 绘制 | 素材获取后合成 |
| `external-ai` | AI 生成 | 输出 prompt，等待外部结果 |

## 平台尺寸规范

| 平台 | 类型 | 推荐尺寸 |
|------|------|----------|
| 小红书 | 封面 | 1080x1440 (3:4) |
| 小红书 | 内页 | 1080x1080 (1:1) |
| 今日头条 | 封面 | 1280x720 (16:9) |
| 微信公众号 | 封面 | 900x383 (2.35:1) |

## 输出要求

每张图输出必须包含：

1. **最终 PNG 文件** - 用于发布
2. **中间 HTML/SVG 文件** - 用于追溯和修改
3. **规范化后的 spec 备份** - 记录生成参数
4. **渲染日志** - 记录执行过程

## 与其他技能协作

| 技能 | 协作内容 |
|------|----------|
| `visual-planner` | 读取 spec，理解图像任务 |
| `asset-sourcer` | 获取外部素材（如需） |
| `image-compose-local` | 执行二次编辑（如需） |
| `smart-cropper` | 智能裁剪（如需） |
| `background-remover` | 去背景处理（如需） |
| `cover-layout-maker` | 封面排版（如需） |
| `image-export-qc` | 导出质检 |
| `visual-reviewer` | 接受审核 |

## 使用示例

### 示例 1：完整的封面生成

```bash
# visual_plan.md 内容：
# ### 01_cover
# - id: 01_cover
# - purpose: 封面
# - template: cover-alert
# - title: "AI 安全工具 OpenClaw"
# - subtitle: "高危漏洞预警"
# - ratio: 3:4

/image-card-builder openclaw-analysis --plan topics/openclaw-analysis/fig/visual_plan.md
```

### 示例 2：引用卡片批量生成

```bash
# visual_plan.md 内容：
# ### 02_quote_01
# - id: 02_quote_01
# - template: quote-card
# - quote: "第一句引用"
#
# ### 03_quote_02
# - id: 03_quote_02
# - template: quote-card
# - quote: "第二句引用"

/image-card-builder quotes-topic --plan topics/quotes-topic/fig/visual_plan.md
```

### 示例 3：指定模板风格

```bash
/image-card-builder ai-topic --plan visual_plan.md --theme cute-tech
```

### 示例 4：预览模式

```bash
/image-card-builder test-topic --plan visual_plan.md --dry-run
```

## 执行日志格式

```markdown
# 图像执行日志

**主题**: {topic-name}
**执行开始**: {timestamp}
**执行完成**: {timestamp}

---

## 01_cover

### Spec 意图
- purpose: 封面
- template: cover-alert
- title: AI 安全工具 OpenClaw

### 执行过程
- 使用模板：cover-alert
- 渲染引擎：HTML/CSS + Playwright
- 输出尺寸：1080x1440

### 最终输出
- 文件：fig/output/01_cover.png
- 中间文件：fig/intermediate/01_cover.html
- 状态：✅ 成功
```

## 错误处理

| 错误 | 处理方式 |
|------|----------|
| spec 字段缺失 | 报错并说明缺少哪个字段 |
| 模板不存在 | 使用兜底模板 cover-minimal |
| 素材文件不存在 | 记录错误，跳过该图片 |
| Playwright 不可用 | 尝试用 node-canvas 兜底 |
| 字体缺失 | 使用系统默认字体 |
| 输出路径无权限 | 输出到当前目录并提示 |

## 环境要求

- Node.js 16+
- Playwright (`npm install playwright`)
- Pillow（Python 兜底方案）

## 安装依赖

```bash
cd .claude/skills/image-card-builder
npm install playwright
# 或
pip install pillow
```

## 最佳实践

1. **先验证 spec 完整性** - 确保字段齐全
2. **选择合适的模板** - 根据 purpose 和 visual_tone
3. **保存中间文件** - 便于追溯和修改
4. **记录执行日志** - 方便排查问题
5. **使用主题系统** - 保持整套图风格统一
6. **优先 HTML/CSS** - 除非有特殊理由
7. **接受 reviewer 审核** - 根据意见调整

## 与 visual-planner 的交接

- 读取 visual_plan.md 中的图片执行脚本
- 严格遵守 spec 定义的意图
- 不得偏离 theme_anchor 和 visual_goal
- 在 builder_freedom 范围内可做审美优化

## 与 visual-reviewer 的交接

- 输出完成后通知 reviewer 审核
- 根据审核意见进行返工
- 返工后重新输出并记录日志
- 只有 pass 后才能进入发布流程
