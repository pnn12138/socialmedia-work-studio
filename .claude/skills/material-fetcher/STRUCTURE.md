# 智能素材搜索工作流 - 文件结构总结

## 完整文件树

```
.claude/
├── agents/
│   └── material-fetcher.md       # Agent 配置：角色定位、触发条件、核心能力
│
├── rules/
│   ├── material-fetch.md         # 质量规则：评估标准、优先级、重试策略
│   └── material-fetch-report.md  # 报告模板：生成报告的结构
│
├── hooks/
│   └── material-fetch.md         # 钩子配置：前后置处理
│
└── skills/
    └── material-fetcher/
        ├── SKILL.md              # 技能定义：命令格式、使用示例
        ├── CLAUDE.md             # 模块说明：架构概览、各层职责
        ├── WORKFLOW.md           # 工作流详解：Phase 1/2/3
        ├── ENHANCEMENT_PLAN.md   # 扩展计划
        ├── index.js              # 主入口
        ├── package.json
        │
        ├── fetchers/
        │   ├── github-fetcher.js     # GitHub 资源获取
        │   ├── web-assets.js         # 官网品牌资产获取
        │   ├── web-crawler.js        # 官网子页面爬虫（待实现）
        │   ├── logo-api.js           # Clearbit/Brandfetch API（待实现）
        │   ├── logo-grabber.js       # Logo 聚合搜索
        │   └── xhs-downloader.js     # 小红书下载（需扩展 MCP）
        │
        ├── downloaders/
        │   └── universal.js          # 通用下载器
        │
        ├── utils/
        │   ├── url-extractor.js      # URL 提取
        │   ├── quality-assess.js     # 质量评估（待实现）
        │   └── color-extract.js      # 颜色提取（待实现）
        │
        └── templates/
            └── report.md             # 报告模板 JS 版（待实现）
```

## 各层说明

### 1. Agent 层 (`.claude/agents/material-fetcher.md`)

**用途**：定义 Claude 在素材获取任务中的角色和行为

**核心内容**：
- 角色定位：素材搜索与获取专家
- 触发条件：何时激活此 Agent
- 核心能力：多平台爬取、质量评估、智能重试、报告生成
- 工作流程：Phase 1 → Phase 2 → Phase 3
- 输出规范：保存路径、命名规范

**使用场景**：
```
用户：帮我获取 OpenClaw 的 Logo 和素材
→ 激活 material-fetcher Agent
→ 执行完整工作流
```

---

### 2. Rules 层 (`.claude/rules/`)

**material-fetch.md** - 质量规则：

**用途**：定义素材质量标准和操作规范

**核心内容**：
- Logo 质量标准（S/A/B/C/D 级）
- 评分公式
- 爬取平台优先级（P0/P1/P2）
- 文件命名规范
- 版权与合规
- 重试策略

**使用场景**：
```javascript
// 质量评估时引用规则
if (qualityScore < 60) {
  // 标记为 D 级，建议人工替换
}
```

---

**material-fetch-report.md** - 报告模板：

**用途**：定义《素材获取报告》的结构

**核心内容**：
- 报告 Markdown 模板
- 质量评分说明
- 用户确认指令

**使用场景**：
```
生成报告时，按此模板填充内容
```

---

### 3. Hooks 层 (`.claude/hooks/material-fetch.md`)

**用途**：定义素材获取流程中的前后置钩子

**钩子列表**：
| 钩子 | 触发时机 |
|------|----------|
| `before-fetch` | 开始素材获取前 |
| `before-crawl` | 爬取每个平台前 |
| `after-fetch` | 单个平台爬取完成后 |
| `after-all-fetch` | 所有平台爬取完成后 |
| `quality-check` | 质量评估完成后 |
| `report-generated` | 报告生成完成后 |
| `user-confirmed` | 用户确认素材后 |

**使用场景**：
```json
{
  "event": "before-fetch",
  "handler": "prepare-fetch-context"
}
```

---

### 4. Skills 层 (`.claude/skills/material-fetcher/`)

**用途**：实际执行的代码实现

#### SKILL.md - 技能定义

**核心内容**：
- 命令格式（完整工作流/分步/传统模式）
- 执行流程
- 质量评估标准
- 钩子触发说明
- 失败处理

**使用示例**：
```bash
# 完整工作流
/material-fetcher workflow:start OpenClaw

# 分步执行
/material-fetcher crawl OpenClaw
/material-fetcher evaluate
/material-fetcher report
/material-fetcher confirm
```

---

#### CLAUDE.md - 模块说明

**核心内容**：
- 架构概览（各层职责）
- 使用方式
- 支持的渠道
- 质量标准
- 版权与合规

---

#### WORKFLOW.md - 工作流详解

**核心内容**：
- 工作流架构图
- Phase 1: 多平台并行爬取
- Phase 2: 质量评估与智能重试
- Phase 3: 用户核对报告
- 实现计划

---

#### 代码实现

**fetchers/** - 各平台 Fetcher：
- `github-fetcher.js` - GitHub 资源获取 ✅
- `web-assets.js` - 官网首页资产获取 ✅
- `web-crawler.js` - 官网子页面爬虫 ⚪
- `logo-api.js` - Clearbit/Brandfetch API ⚪
- `logo-grabber.js` - Logo 聚合搜索 ✅
- `xhs-downloader.js` - 小红书下载 ⚪

**downloaders/** - 下载器：
- `universal.js` - 通用 HTTP 下载器 ✅

**utils/** - 工具函数：
- `url-extractor.js` - URL 提取 ✅
- `quality-assess.js` - 质量评估 ⚪
- `color-extract.js` - 颜色提取 ⚪

---

## 数据流与调用关系

```
用户请求
    ↓
[Agent 层] material-fetcher.md
    ↓ 激活
[Rules 层] material-fetch.md (质量标准)
    ↓ 指导
[Skills 层] index.js → workflow/
    ↓ 执行 Phase 1
fetchers/*.js → 爬取平台
    ↓
downloaders/universal.js → 下载文件
    ↓
[Hooks 层] before-crawl / after-fetch
    ↓ 前后置处理
[Skills 层] utils/quality-assess.js → 质量评估
    ↓ 参照
[Rules 层] material-fetch.md (评分标准)
    ↓
[Hooks 层] quality-check
    ↓ 决定是否重试
[Skills 层] workflow/phase2-retry.js
    ↓
[Skills 层] workflow/phase3-report.js → 生成报告
    ↓ 使用模板
[Rules 层] material-fetch-report.md
    ↓
[Hooks 层] report-generated → 通知用户
    ↓
用户核对
    ↓
[Hooks 层] user-confirmed → finalize
```

---

## 文件状态

| 文件 | 状态 | 说明 |
|------|------|------|
| `agents/material-fetcher.md` | ✅ | Agent 配置 |
| `rules/material-fetch.md` | ✅ | 质量规则 |
| `rules/material-fetch-report.md` | ✅ | 报告模板 |
| `hooks/material-fetch.md` | ✅ | 钩子配置 |
| `skills/material-fetcher/SKILL.md` | ✅ | 技能定义 |
| `skills/material-fetcher/CLAUDE.md` | ✅ | 模块说明 |
| `skills/material-fetcher/WORKFLOW.md` | ✅ | 工作流详解 |
| `skills/material-fetcher/ENHANCEMENT_PLAN.md` | ✅ | 扩展计划 |
| `skills/material-fetcher/index.js` | ✅ | 主入口 |
| `skills/material-fetcher/fetchers/*.js` | 部分 | 各平台 Fetcher |

---

## 下一步实现

根据 `ENHANCEMENT_PLAN.md`：

1. **P0 - 第三方 Logo API**
   - `fetchers/logo-api.js` - Clearbit/Google Favicon

2. **P0 - 网站爬虫**
   - `fetchers/web-crawler.js` - 子页面爬取

3. **P1 - 质量评估**
   - `utils/quality-assess.js` - 质量评估函数

4. **P1 - 报告生成**
   - `workflow/phase3-report.js` - 报告生成器
