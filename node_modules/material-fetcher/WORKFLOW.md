# 智能素材搜索工作流 (Intelligent Material Search Workflow)

## 工作流目标

建立一个**自动化 + 人工核对**的素材搜索系统，包含：
1. 多平台自动爬取
2. 智能评估与重试
3. 用户核对与人工补充

---

## 工作流架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                    智能素材搜索工作流                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  输入：品牌名/项目名/官网 URL                                        │
│         ↓                                                           │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ Phase 1: 多平台并行爬取 (Multi-Platform Crawl)                │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐│ │
│  │  │ GitHub  │ │ 官网    │ │Clearbit │ │ Google  │ │Brandfetch││ │
│  │  │Fetcher  │ │Crawler  │ │ API     │ │Favicon  │ │ API     ││ │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘│ │
│  │       └───────────┴───────────┴───────────┴───────────┘      │ │
│  │                              ↓                                │ │
│  │                    素材聚合池 (Material Pool)                 │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                              ↓                                      │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ Phase 2: 质量评估与智能重试 (Quality Check & Retry)           │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │  评估标准：                                                   │ │
│  │  - SVG 优先？→ 是：标记为最佳候选                              │ │
│  │  - 分辨率>256x256？→ 是：通过                                  │ │
│  │  - 有透明背景？→ 是：加分                                      │ │
│  │                              ↓                                │ │
│  │  如果未找到 SVG 或高质量 Logo → 触发 Phase 1b 深度爬取          │ │
│  │  - 爬取 /brand, /press, /media, /about 页面                    │ │
│  │  - 搜索 CDN、子域名                                            │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                              ↓                                      │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ Phase 3: 用户核对报告 (User Review Report)                    │ │
│  ├───────────────────────────────────────────────────────────────┤ │
│  │  生成《素材获取报告》包含：                                   │ │
│  │  ✅ 已获取素材清单（带质量评分）                               │ │
│  │  ⚠️  低质量素材标记（需要人工替换）                            │ │
│  │  ❌ 未找到的素材清单（需要人工搜索）                           │ │
│  │  📋 人工搜索建议（关键词 + 来源）                              │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                              ↓                                      │
│  输出：素材包 + 报告 + 人工任务清单                                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: 多平台并行爬取

### 1.1 支持的爬取平台

| 平台 | 类型 | 优先级 | 说明 |
|------|------|--------|------|
| **GitHub** | 代码托管 | P0 | 获取项目 Logo、README 图片、Assets |
| **官网 (首页)** | 官方网站 | P0 | 获取 favicon、meta 中的 Logo |
| **官网 (子页面)** | 品牌页面 | P1 | /brand、/press、/media、/about |
| **Clearbit** | Logo API | P0 | 高清 Logo 一键获取 |
| **Google Favicon** | Favicon 服务 | P0 | 快速 favicon 获取 |
| **Brandfetch** | 品牌 API | P1 | 品牌资产聚合 |
| **DuckDuckGo Images** | 图片搜索 | P2 | 备选方案 |
| **Bing Images** | 图片搜索 | P2 | 备选方案 |

### 1.2 执行流程

```javascript
// 伪代码示例
async function multiPlatformFetch(target, outputDir) {
  const results = {
    logo: [],
    icons: [],
    screenshots: [],
    references: []
  };

  // 解析目标
  const { brandName, domain, githubRepo } = parseTarget(target);

  // 并行执行所有 P0 来源
  const p0Tasks = [
    fetchGitHub(githubRepo, outputDir),
    fetchWebsiteHome(domain, outputDir),
    fetchClearbit(domain, outputDir),
    fetchGoogleFavicon(domain, outputDir)
  ];

  await Promise.all(p0Tasks);

  // 初步评估
  const quality = assessQuality(results.logo);

  // 如果质量不够，执行 P1 来源
  if (!quality.hasSVG || quality.maxResolution < 256) {
    const p1Tasks = [
      fetchWebsiteSubPages(domain, outputDir),
      fetchBrandfetch(domain, outputDir)
    ];
    await Promise.all(p1Tasks);
  }

  return results;
}
```

---

## Phase 2: 质量评估与智能重试

### 2.1 质量评估标准

```javascript
const qualityCriteria = {
  // 格式优先级
  format: {
    SVG: 100,    // 最佳 - 可无限缩放
    PNG: 80,     // 优秀 - 支持透明
    WEBP: 70,    // 良好
    JPG: 50,     // 一般
    ICO: 30      // 较差 - 仅 favicon
  },

  // 分辨率要求
  resolution: {
    excellent: 512,   // ≥512px
    good: 256,        // ≥256px
    acceptable: 128,  // ≥128px
    poor: 0           // <128px
  },

  // 透明背景加分
  transparent: +20,

  // 文件尺寸（不过大）
  fileSize: {
    optimal: 50 * 1024,    // <50KB
    acceptable: 200 * 1024 // <200KB
  }
};
```

### 2.2 评估函数

```javascript
function assessQuality(logos) {
  return {
    hasSVG: logos.some(l => l.format === 'svg'),
    maxResolution: Math.max(...logos.map(l => l.width)),
    bestCandidate: logos.sort((a, b) => b.score - a.score)[0],
    needsRetry: !logos.some(l => l.format === 'svg' && l.width >= 256),
    scoreDistribution: logos.map(l => l.score)
  };
}
```

### 2.3 重试策略

| 触发条件 | 重试动作 | 最大重试次数 |
|----------|----------|--------------|
| 无 SVG Logo | 深度爬取子页面 | 1 次 |
| 无>256px Logo | 尝试 Brandfetch API | 1 次 |
| 无透明 Logo | 尝试背景移除技能 | 1 次 |
| 官网无法访问 | 尝试 Wayback Machine | 1 次 |
| GitHub 404 | 搜索镜像仓库 | 1 次 |

---

## Phase 3: 用户核对报告

### 3.1 报告结构

```markdown
# 素材获取报告 - [品牌/项目名]

**生成时间**: 2026-03-10 15:30

---

## 执行摘要

- 爬取平台数：6
- 获取素材总数：12
- 最佳质量素材：logo_clearbit_openclaw.ai.png (SVG, 512x512)
- 需要人工补充：2 项

---

## ✅ 已获取素材清单

| 文件名 | 来源 | 格式 | 分辨率 | 质量评分 | 推荐用途 |
|--------|------|------|--------|----------|----------|
| logo_clearbit_openclaw.ai.png | Clearbit | PNG | 512x512 | 95 | 封面主 Logo |
| logo_openclaw_favicon.svg | 官网 | SVG | 64x64 | 90 | 小尺寸场景 |
| logo_openclaw_org.png | GitHub | PNG | 400x400 | 75 | 备选 |

---

## ⚠️ 低质量素材标记

以下素材质量较低，建议人工替换：

| 文件名 | 问题 | 建议 |
|--------|------|------|
| logo_google_openclaw.ai.png | 分辨率仅 32x32 | 从官网下载高清版本 |

---

## ❌ 未找到的素材

以下素材未能自动获取，需要人工搜索：

| 素材类型 | 建议搜索关键词 | 建议来源 |
|----------|---------------|----------|
| 应用界面截图 | OpenClaw UI screenshot | 官方文档 |
| 品牌色卡 | OpenClaw brand colors | /brand 页面 |

---

## 📋 人工搜索建议

### 1. OpenClaw 官方 Logo (SVG 优先)
- **搜索词**: `OpenClaw AI brand assets`、`OpenClaw logo svg download`
- **来源**: `https://openclaw.ai/brand` (如有)
- **保存路径**: `fig/素材/logo_openclaw_official.svg`

### 2. 应用界面截图
- **搜索词**: `OpenClaw dashboard screenshot`
- **来源**: GitHub README、官方文档
- **保存路径**: `fig/素材/screenshot_ui.png`

---

## 下一步行动

1. 检查上述「低质量素材」是否需要替换
2. 按照「人工搜索建议」下载缺失素材
3. 完成后执行：`/material-fetcher review` 确认
```

### 3.2 用户核对流程

```
1. 系统生成《素材获取报告》
   ↓
2. 用户查看报告，确认：
   - [ ] 最佳候选 Logo 是否满意
   - [ ] 低质量素材是否需要替换
   - [ ] 缺失素材是否必须
   ↓
3. 用户执行：
   A. 满意 → `/material-fetcher confirm` 进入下一步
   B. 需要补充 → 人工搜索后 `/material-fetcher review` 重新评估
   ↓
4. 素材确认完成，进入视觉生成阶段
```

---

## 目录结构扩展

```
material-fetcher/
├── workflow/
│   ├── index.js              # 工作流主控制器
│   ├── phase1-crawler.js     # Phase 1 多平台爬取
│   ├── phase2-evaluator.js   # Phase 2 质量评估
│   └── phase3-report.js      # Phase 3 报告生成
├── fetchers/
│   ├── github-fetcher.js     # GitHub
│   ├── web-crawler.js        # 官网爬虫（支持子页面）
│   ├── logo-api.js           # Clearbit/Brandfetch
│   └── search-engine.js      # 搜索引擎图片
├── utils/
│   ├── quality-assess.js     # 质量评估
│   ├── color-extract.js      # 颜色提取
│   └── url-discover.js       # URL 发现
└── templates/
    └── report.md             # 报告模板
```

---

## 实现计划

| 阶段 | 任务 | 预计时间 |
|------|------|----------|
| **Phase 1** | 多平台爬取框架 | 3h |
| - | Clearbit/Google Favicon API | 1h |
| - | 官网子页面爬虫 | 2h |
| **Phase 2** | 质量评估模块 | 1h |
| - | 智能重试逻辑 | 1h |
| **Phase 3** | 报告生成模板 | 1h |
| - | 用户核对流程 | 1h |

---

## 使用示例

```bash
# 完整工作流
/material-fetcher workflow:start openclaw

# 仅执行 Phase 1（爬取）
/material-fetcher crawl openclaw --platforms=github,web,clearbit

# 仅执行 Phase 2（评估）
/material-fetcher evaluate

# 仅执行 Phase 3（报告）
/material-fetcher report

# 重新评估（人工补充后）
/material-fetcher review
```
