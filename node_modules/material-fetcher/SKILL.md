---
name: material-fetcher
argument-hint: "[workflow:start|crawl|evaluate|report|review] [target] [options]"
description: |
  素材获取模块，支持从 GitHub、官网、小红书等渠道获取品牌资产、Logo、截图等素材。
  当需要获取项目 Logo、官网品牌资产、小红书笔记图片时使用。

  相关配置:
  - Agent: `.claude/agents/material-fetcher.md`
  - Rules: `.claude/rules/material-fetch.md`
  - Hooks: `.claude/hooks/material-fetch.md`
---

## 命令格式

### 完整工作流模式

```
/material-fetcher workflow:start <target>
```

### 分步执行模式

```
/material-fetcher crawl <target> [--platforms=github,web,clearbit]
/material-fetcher evaluate
/material-fetcher report
/material-fetcher review
/material-fetcher confirm
```

### 传统模式（兼容）

```
/material-fetcher <source>:<identifier> [type:<类型>] [output:<路径>]
```

## 支持的源

| 源 | 格式 | 说明 |
|------|------|------|
| **GitHub** | `github:<user/repo>` | 获取项目 Logo、截图、Assets |
| **Web** | `web:<url>` | 获取官网 Logo、favicon、OG Image |
| **小红书** | `xhs:<feed_id 或 URL>` | 下载笔记图片 |
| **Logo 聚合** | `logo:<品牌名>` | 多源搜索 Logo |

## type 参数

| 源 | 可选值 | 默认 |
|------|--------|------|
| GitHub | `logo`、`screenshot`、`assets`、`all` | `all` |
| Web | `logo`、`screenshot`、`all` | `all` |
| 小红书 | `images` | `images` |
| Logo | `all` | `all` |

## 使用示例

### 完整工作流（推荐）

```bash
# 启动完整工作流（自动爬取 + 评估 + 报告）
/material-fetcher workflow:start OpenClaw
/material-fetcher workflow:start https://openclaw.ai
```

### 分步执行

```bash
# 仅执行爬取
/material-fetcher crawl OpenClaw --platforms=github,web,clearbit

# 仅执行评估
/material-fetcher evaluate

# 仅生成报告
/material-fetcher report

# 人工补充后重新评估
/material-fetcher review

# 确认素材
/material-fetcher confirm
```

### 传统模式

```bash
# 获取 OpenClaw 的 Logo
/material-fetcher github:openclaw/openclaw type:logo

# 获取官网所有品牌资产
/material-fetcher web:https://openclaw.ai type:all

# 下载小红书笔记图片
/material-fetcher xhs:664a0f03000000002f006f9e

# 聚合搜索 Logo
/material-fetcher logo:OpenClaw
```

## 执行流程

### 完整工作流模式

```
1. 接收任务 → hook:before-fetch
   ↓
2. Phase 1: 多平台并行爬取
   - GitHub Fetcher
   - Web Crawler (首页 + 子页面)
   - Clearbit API
   - Google Favicon
   - Brandfetch API (条件触发)
   ↓
3. Phase 2: 质量评估
   - 格式检查 (SVG > PNG > ...)
   - 分辨率检查 (≥256px)
   - 智能重试决策
   ↓
4. Phase 3: 生成报告
   - 已获取素材清单
   - 低质量素材标记
   - 人工搜索建议
   ↓
5. 用户核对
   - 满意 → confirm
   - 需补充 → 人工搜索后 review
```

### 分步模式

```
crawl → evaluate → report → [review] → confirm
```

## 质量评估标准

参照 `.claude/rules/material-fetch.md`

| 等级 | 格式 | 分辨率 | 评分 |
|------|------|--------|------|
| **S** | SVG | 任意 | 90-100 |
| **A** | PNG | ≥512x512 | 80-89 |
| **B** | PNG | ≥256x256 | 70-79 |
| **C** | PNG/JPG | ≥128x128 | 60-69 |
| **D** | 任意 | <128x128 | <60 |

## 报告生成

报告模板参照 `.claude/rules/material-fetch-report.md`

### 报告结构

1. 执行摘要
2. ✅ 已获取素材清单
3. ⚠️ 低质量素材标记
4. ❌ 未找到的素材
5. 📋 人工搜索建议
6. 下一步行动

## 钩子触发

参照 `.claude/hooks/material-fetch.md`

| 钩子 | 触发时机 |
|------|----------|
| `before-fetch` | 开始素材获取前 |
| `before-crawl` | 爬取每个平台前 |
| `after-fetch` | 单个平台爬取完成后 |
| `after-all-fetch` | 所有平台爬取完成后 |
| `quality-check` | 质量评估完成后 |
| `report-generated` | 报告生成完成后 |
| `user-confirmed` | 用户确认素材后 |

## 失败处理

| 场景 | 处理 |
|------|------|
| GitHub 仓库不存在 | 告知用户检查仓库名，尝试搜索镜像 |
| 官网无法访问 | 建议检查 URL 或网络，尝试 Wayback Machine |
| 小红书未登录 | 引导使用 xhs-login |
| 笔记已删除 | 告知用户笔记不可访问 |
| Logo 未找到 | 触发深度爬取，生成人工搜索建议 |
| 质量不达标 | 标记低质量，建议人工替换 |

## 约束条件

1. 小红书图片下载需已安装并登录 xiaohongshu-mcp
2. GitHub API 有速率限制（未认证 60 次/小时）
3. 商用素材必须验证版权
4. 品牌 Logo 用于评论/分析类内容属于合理使用

## 依赖

- Node.js 18+
- `.claude/agents/material-fetcher.md` - Agent 配置
- `.claude/rules/material-fetch.md` - 质量规则
- `.claude/hooks/material-fetch.md` - 钩子配置
- `.claude/rules/material-fetch-report.md` - 报告模板

## 相关文件

```
.claude/
├── agents/material-fetcher.md    # Agent 配置
├── rules/
│   ├── material-fetch.md         # 质量规则
│   └── material-fetch-report.md  # 报告模板
├── hooks/material-fetch.md       # 钩子配置
└── skills/
    └── material-fetcher/
        ├── WORKFLOW.md           # 工作流说明
        └── ...
```
