# 智能素材搜索工作流 - 实现完成总结

## 工作流解耦完成

已将智能素材搜索工作流完整解耦到 Claude Code 的文件体系中：

---

## 文件结构

```
.claude/
├── agents/
│   └── material-fetcher.md       ✅ Agent 配置（角色定位、触发条件）
│
├── rules/
│   ├── material-fetch.md         ✅ 质量规则（评估标准、优先级）
│   └── material-fetch-report.md  ✅ 报告模板（生成报告结构）
│
├── hooks/
│   └── material-fetch.md         ✅ 钩子配置（前后置处理）
│
└── skills/material-fetcher/
    ├── SKILL.md                  ✅ 技能定义（命令格式）
    ├── CLAUDE.md                 ✅ 模块说明（架构概览）
    ├── WORKFLOW.md               ✅ 工作流详解（Phase 1/2/3）
    ├── STRUCTURE.md              ✅ 文件结构总结
    ├── ENHANCEMENT_PLAN.md       ✅ 扩展计划
    ├── index.js                  ✅ 主入口
    ├── package.json
    │
    ├── fetchers/                 ✅ 各平台 Fetcher（部分完成）
    ├── downloaders/              ✅ 下载器
    └── utils/                    ✅ 工具函数（部分完成）
```

---

## 各层职责

### 1. Agent 层 - `.claude/agents/material-fetcher.md`

**职责**：定义 Claude 在素材获取任务中的角色

**核心内容**：
- 角色：素材搜索与获取专家
- 触发条件：Logo 获取、品牌资产搜索等
- 核心能力：多平台爬取、质量评估、智能重试、报告生成
- 工作流程：Phase 1 → Phase 2 → Phase 3

---

### 2. Rules 层 - `.claude/rules/`

**material-fetch.md** - 质量规则：
- Logo 质量标准（S/A/B/C/D 级）
- 评分公式（格式 + 分辨率 + 附加分）
- 爬取平台优先级（P0/P1/P2）
- 文件命名规范
- 版权与合规
- 重试策略

**material-fetch-report.md** - 报告模板：
- 报告 Markdown 结构
- 质量评分说明
- 用户确认指令

---

### 3. Hooks 层 - `.claude/hooks/material-fetch.md`

**职责**：定义前后置处理钩子

| 钩子 | 触发时机 |
|------|----------|
| `before-fetch` | 开始素材获取前 |
| `before-crawl` | 爬取每个平台前 |
| `after-fetch` | 单个平台爬取完成后 |
| `after-all-fetch` | 所有平台爬取完成后 |
| `quality-check` | 质量评估完成后 |
| `report-generated` | 报告生成完成后 |
| `user-confirmed` | 用户确认素材后 |

---

### 4. Skills 层 - `.claude/skills/material-fetcher/`

**职责**：实际执行的代码实现

**核心文件**：
| 文件 | 状态 | 说明 |
|------|------|------|
| `SKILL.md` | ✅ | 技能定义（完整工作流/分步/传统模式） |
| `CLAUDE.md` | ✅ | 模块说明（架构概览、各层职责） |
| `WORKFLOW.md` | ✅ | 工作流详解（多平台爬取、评估、报告） |
| `STRUCTURE.md` | ✅ | 文件结构总结 |
| `ENHANCEMENT_PLAN.md` | ✅ | 扩展计划（Clearbit、爬虫等） |
| `index.js` | ✅ | 主入口（命令解析） |

**Fetcher 实现**：
| Fetcher | 状态 | 说明 |
|---------|------|------|
| `github-fetcher.js` | ✅ | GitHub 资源获取 |
| `web-assets.js` | ✅ | 官网首页资产获取 |
| `logo-grabber.js` | ✅ | Logo 聚合搜索 |
| `web-crawler.js` | ⚪ | 官网子页面爬虫（待实现） |
| `logo-api.js` | ⚪ | Clearbit/Brandfetch API（待实现） |
| `xhs-downloader.js` | ⚪ | 小红书下载（需扩展 MCP） |

---

## 使用方式

### 完整工作流（推荐）

```bash
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

---

## 工作流执行流程

```
1. 用户请求
   ↓
2. Agent 层激活 (material-fetcher.md)
   ↓
3. Rules 层指导 (material-fetch.md)
   ↓
4. Phase 1: 多平台并行爬取
   - GitHub Fetcher
   - Web Assets Fetcher
   - Clearbit API (待实现)
   - Google Favicon (待实现)
   ↓
5. Phase 2: 质量评估
   - 格式检查 (SVG > PNG > ...)
   - 分辨率检查 (≥256px)
   - 智能重试决策
   ↓
6. Phase 3: 生成报告
   - 使用 rules/material-fetch-report.md 模板
   - 包含：已获取清单、低质量标记、人工建议
   ↓
7. 用户核对
   - 满意 → confirm
   - 需补充 → 人工搜索后 review
   ↓
8. Hooks 层 finalize (user-confirmed)
```

---

## 质量标准

| 等级 | 格式 | 分辨率 | 评分 | 说明 |
|------|------|--------|------|------|
| **S** | SVG | 任意 | 90-100 | 最佳 |
| **A** | PNG | ≥512x512 | 80-89 | 优秀 |
| **B** | PNG | ≥256x256 | 70-79 | 良好 |
| **C** | PNG/JPG | ≥128x128 | 60-69 | 可用 |
| **D** | 任意 | <128x128 | <60 | 不推荐 |

---

## 智能重试策略

| 触发条件 | 重试动作 | 最大次数 |
|----------|----------|----------|
| 无 SVG Logo | 深度爬取子页面 | 1 |
| 无高清 Logo | Brandfetch API | 1 |
| 官网 404 | Wayback Machine | 1 |
| GitHub 404 | 搜索镜像 | 1 |

---

## 用户核对报告示例

```markdown
# 素材获取报告 - OpenClaw

**生成时间**: 2026-03-10 15:30

---

## 执行摘要

- 爬取平台数：4
- 获取素材总数：9
- 最佳质量素材：logo_openclaw_favicon.svg (SVG, 64x64)
- 需要人工补充：2 项

---

## ✅ 已获取素材清单

| 文件名 | 来源 | 格式 | 分辨率 | 质量评分 | 推荐用途 |
|--------|------|------|--------|----------|----------|
| logo_openclaw_favicon.svg | 官网 | SVG | 64x64 | 90 | 封面主 Logo |
| logo_openclaw_org.png | GitHub | PNG | 400x400 | 75 | 备选 |

---

## ⚠️ 低质量素材标记

| 文件名 | 问题 | 建议 |
|--------|------|------|
| - | - | - |

---

## ❌ 未找到的素材

| 素材类型 | 建议搜索关键词 | 建议来源 |
|----------|---------------|----------|
| 应用界面截图 | OpenClaw UI screenshot | 官方文档 |
| ClawJacked 漏洞图 | ClawJacked Oasis Security | 技术报告 |

---

## 下一步行动

1. [ ] 确认最佳候选 Logo 是否满意
2. [ ] 人工搜索缺失素材（见上方建议）
3. [ ] 完成后回复：`/material-fetcher confirm`
```

---

## 待实现功能

根据 `ENHANCEMENT_PLAN.md`：

1. **P0 - 第三方 Logo API**
   - `fetchers/logo-api.js` - Clearbit/Google Favicon

2. **P0 - 网站爬虫**
   - `fetchers/web-crawler.js` - 子页面爬取

3. **P1 - 质量评估**
   - `utils/quality-assess.js` - 质量评估函数

4. **P1 - 报告生成**
   - 自动化报告生成器

---

## 相关文件清单

| 文件 | 状态 | 行数 |
|------|------|------|
| `.claude/agents/material-fetcher.md` | ✅ | ~90 |
| `.claude/rules/material-fetch.md` | ✅ | ~150 |
| `.claude/rules/material-fetch-report.md` | ✅ | ~100 |
| `.claude/hooks/material-fetch.md` | ✅ | ~150 |
| `.claude/skills/material-fetcher/SKILL.md` | ✅ | ~150 |
| `.claude/skills/material-fetcher/CLAUDE.md` | ✅ | ~120 |
| `.claude/skills/material-fetcher/WORKFLOW.md` | ✅ | ~300 |
| `.claude/skills/material-fetcher/STRUCTURE.md` | ✅ | ~250 |
| `.claude/skills/material-fetcher/ENHANCEMENT_PLAN.md` | ✅ | ~240 |

**总计**：~1550 行文档 + 代码实现
