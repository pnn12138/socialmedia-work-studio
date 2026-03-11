# Material Fetcher - 素材获取模块

## 模块目标

为 AI 内容生产提供**一站式素材获取能力**，支持从多渠道自动获取品牌资产、Logo、截图、参考图等素材。

## 架构概览

```
素材获取模块采用解耦设计，分散到 Claude Code 的不同配置层：

.claude/
├── agents/material-fetcher.md       # Agent 配置（角色与能力）
├── rules/
│   ├── material-fetch.md            # 质量规则与标准
│   └── material-fetch-report.md     # 报告模板
├── hooks/material-fetch.md          # 钩子配置（前后置处理）
└── skills/material-fetcher/         # 技能实现（代码）
    ├── SKILL.md                     # 技能定义
    ├── WORKFLOW.md                  # 工作流说明
    ├── fetchers/                    # 各平台 Fetcher
    ├── downloaders/                 # 下载器
    └── utils/                       # 工具函数
```

## 各层职责

### Agent 层 (`.claude/agents/material-fetcher.md`)

**职责**：定义角色定位、触发条件、核心能力

**内容**：
- 角色：素材搜索与获取专家
- 触发条件：Logo 获取、品牌资产搜索等
- 核心能力：多平台爬取、质量评估、智能重试、报告生成
- 工作流程：Phase 1 → Phase 2 → Phase 3

### Rules 层 (`.claude/rules/`)

**material-fetch.md** - 质量规则与标准：
- Logo 质量标准（S/A/B/C/D 级）
- 评分公式
- 爬取平台优先级（P0/P1/P2）
- 文件命名规范
- 版权与合规
- 重试策略

**material-fetch-report.md** - 报告模板：
- 报告结构
- 质量评分说明
- 用户确认指令

### Hooks 层 (`.claude/hooks/material-fetch.md`)

**职责**：定义前后置处理钩子

**钩子列表**：
- `before-fetch` - 准备上下文
- `before-crawl` - 准备爬取平台
- `after-fetch` - 处理结果
- `after-all-fetch` - 聚合结果
- `quality-check` - 处理质量评估
- `report-generated` - 通知用户
- `user-confirmed` - finalize

### Skills 层 (`.claude/skills/material-fetcher/`)

**职责**：实际执行的代码实现

**核心文件**：
- `SKILL.md` - 技能定义与命令格式
- `WORKFLOW.md` - 完整工作流说明
- `index.js` - 主入口
- `fetchers/` - 各平台 Fetcher
- `downloaders/` - 通用下载器
- `utils/` - 工具函数

## 使用方式

### 完整工作流（推荐）

```bash
# 启动完整工作流
/material-fetcher workflow:start OpenClaw
/material-fetcher workflow:start https://openclaw.ai
```

### 分步执行

```bash
/material-fetcher crawl OpenClaw --platforms=github,web,clearbit
/material-fetcher evaluate
/material-fetcher report
/material-fetcher review
/material-fetcher confirm
```

### 传统模式

```bash
/material-fetcher github:openclaw/openclaw type:logo
/material-fetcher web:https://openclaw.ai type:all
/material-fetcher logo:OpenClaw
```

## 支持的渠道

| 渠道 | Fetcher | 状态 | 优先级 |
|------|---------|------|--------|
| **GitHub** | `github-fetcher.js` | ✅ | P0 |
| **官网/Web** | `web-crawler.js` | ✅ | P0 |
| **Clearbit** | `logo-api.js` | ✅ | P0 |
| **Google Favicon** | `logo-api.js` | ✅ | P0 |
| **Brandfetch** | `logo-api.js` | ⚪ | P1 |
| **官网子页面** | `web-crawler.js` | ⚪ | P1 |
| **小红书** | `xhs-downloader.js` | ⚪ | P2 |

## 输出规范

### 保存目录

- 默认：`fig/素材/`
- 可指定：`--output=<path>`

### 命名规范

```
<type>_<source>_<identifier>[_<version>].<ext>

type: logo | icon | screenshot | asset
source: github | clearbit | google | brandfetch | official
```

**示例**：
- `logo_clearbit_openclaw.png`
- `logo_github_openclaw.svg`
- `icon_google_openclaw.ai.png`

## 质量标准

| 等级 | 格式 | 分辨率 | 评分 | 说明 |
|------|------|--------|------|------|
| **S** | SVG | 任意 | 90-100 | 最佳 |
| **A** | PNG | ≥512x512 | 80-89 | 优秀 |
| **B** | PNG | ≥256x256 | 70-79 | 良好 |
| **C** | PNG/JPG | ≥128x128 | 60-69 | 可用 |
| **D** | 任意 | <128x128 | <60 | 不推荐 |

## 版权与合规

| 来源 | 商用 | 署名 | 风险 |
|------|------|------|------|
| GitHub 项目 | ✅ | 建议 | 中 |
| 官网 Logo | ✅ | 通常 | 中 |
| Clearbit | ✅ | 否 | 低 |
| Google Favicon | ✅ | 否 | 低 |
| 小红书笔记 | ❌ | - | 高 |

**原则**：
1. 小红书图片仅学习参考，不商用
2. 品牌 Logo 用于评论/分析属合理使用
3. 优先官方渠道和开源资产
4. 商用内容必须验证授权

## 依赖技能

| 技能 | 用途 |
|------|------|
| `web-screenshot-capture` | 网页截图 |
| `image-finder` | 通用素材搜索 |

## 扩展计划

- [ ] Twitter/X 图片下载
- [ ] Instagram 图片下载
- [ ] Pinterest 图片下载
- [ ] 自建图库索引
