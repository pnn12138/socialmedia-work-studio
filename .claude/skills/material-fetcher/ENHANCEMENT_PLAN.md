# Material Fetcher 技能完善计划

## 当前能力与局限

### ✅ 已有能力

| 模块 | 能力 | 局限 |
|------|------|------|
| **GitHub Fetcher** | 获取仓库文件列表、README 图片、Releases Assets | 无法访问 GitHub 组织头像、Wiki Pages |
| **Web Assets Fetcher** | 解析单个 HTML 页面的 meta 标签提取 Logo | 无法爬取子页面（如/brand、/press） |
| **Universal Downloader** | HTTP/HTTPS 文件下载 | 无并发控制、无进度显示 |
| **Logo Grabber** | 聚合 GitHub + 官网搜索 | 来源有限，无第三方 API |

### ❌ 当前无法完成的任务

1. **自动爬取 Brand/Press 页面**
   - 官网的 Brand/Press/Media 页面通常在不同 URL
   - 当前只能解析首页，无法追踪站内链接

2. **获取更高清 Logo**
   - 无法访问第三方 Logo 库（Clearbit、Brandfetch）
   - 无法比较多个版本选择最佳

3. **网页截图**
   - 与 `web-screenshot-capture` 技能未集成
   - 无法自动截取官网首屏作为参考

4. **动态内容处理**
   - 无法处理 JavaScript 渲染的图片
   - 无法处理需要登录的内容

---

## 需要的工具和扩展

### 1. 网站爬虫模块（新增）

**功能**：爬取网站多个页面，查找 Brand/Press 相关页面

```
fetchers/
└── site-crawler.js    # 站内爬虫
```

**需要的能力**：
- 解析首页，提取所有内部链接
- 识别 Brand/Press/Media/About 等关键词
- 递归爬取这些页面，提取 Logo 链接
- 支持 depth 限制（默认 2 层）

**依赖**：
- Node.js `https`/`http` 模块（已有）
- URL 解析库（内置）
- 简单的 HTML 解析（可手写或用 cheerio）

---

### 2. 第三方 Logo API 集成（新增）

**功能**：从专业 Logo 库获取高清品牌 Logo

```
fetchers/
└── logo-api.js    # 第三方 Logo API
```

**支持的 API**：

| API | 说明 | 认证 |
|-----|------|------|
| **Clearbit Logo API** | `https://logo.clearbit.com/<domain>` | 免费 |
| **Brandfetch API** | `https://api.brandfetch.io/v2/search/<domain>` | 免费（需注册） |
| **Google S2Favicon** | `https://www.google.com/s2/favicons?domain=<domain>` | 免费 |
| **Unsplash Source** | `https://source.unsplash.com/` | 免费 |

**使用示例**：
```javascript
// Clearbit
const logoUrl = `https://logo.clearbit.com/openclaw.ai`;

// Brandfetch
const response = await fetch(`https://api.brandfetch.io/v2/search/openclaw.ai`);
```

---

### 3. 截图集成模块（新增）

**功能**：调用 `web-screenshot-capture` 技能截取网页

```
integrations/
└── screenshot.js    # 截图集成
```

**实现方式**：
- 通过子进程调用 `web-screenshot-capture` 技能
- 或直接使用 Puppeteer/Playwright

**使用场景**：
- 截取官网首屏作为参考图
- 截取 GitHub 仓库 README 渲染效果

---

### 4. 图片质量评估（新增）

**功能**：比较多个 Logo 版本，选择最佳

```
utils/
└── image-quality.js    # 图片质量评估
```

**评估标准**：
- 文件尺寸（优先 SVG > 大 PNG > 小 PNG）
- 分辨率（宽 x 高）
- 格式（SVG > PNG > JPG）
- 是否透明背景

**输出**：
- 排序后的 Logo 列表
- 最佳推荐及理由

---

### 5. 品牌颜色提取（新增）

**功能**：从 Logo 中提取品牌主色调

```
utils/
└── color-extractor.js    # 颜色提取
```

**用途**：
- 为视觉规划提供品牌色参考
- 自动生成配色方案

**实现**：
- 使用 `color-thief-node` 或手写简单版
- 提取 Top 3-5 主色

---

## 优先级与实现顺序

| 优先级 | 模块 | 工作量 | 收益 |
|--------|------|--------|------|
| **P0** | 第三方 Logo API（Clearbit） | 1h | 高 - 快速获取高清 Logo |
| **P0** | 网站爬虫（基础版） | 2h | 高 - 自动发现 Brand 页面 |
| **P1** | 图片质量评估 | 1h | 中 - 自动选择最佳 Logo |
| **P1** | 截图集成 | 1h | 中 - 获取官网参考图 |
| **P2** | 品牌颜色提取 | 1h | 低 - 锦上添花 |
| **P2** | Brandfetch API | 1h | 低 - Clearbit 通常足够 |

---

## 当前推荐的解决方案

### 对于 OpenClaw 素材获取

**已完成**：
- ✅ GitHub 组织头像（`logo_openclaw_org.png`）
- ✅ 官网 favicon.svg（`logo_openclaw_favicon.svg`）
- ✅ 官网 icon PNG（`logo_openclaw_icon.png`）
- ✅ Apple touch icon（`logo_openclaw_apple.png`）
- ✅ README 截图 5 张

**建议下一步**：
1. 使用 `logo_openclaw_favicon.svg` 作为封面 Logo（SVG 格式，可无限缩放）
2. 继续用 AI 生成背景图
3. 使用 `post-builder` 进行排版合成

---

## 技能扩展代码框架

### Clearbit Logo Fetcher（示例）

```javascript
// fetchers/logo-api.js

const https = require('https');
const { downloadFile } = require('../downloaders/universal');

/**
 * 从 Clearbit 获取 Logo
 */
async function fetchClearbit(domain, outputDir) {
  const logoUrl = `https://logo.clearbit.com/${domain}`;
  const filename = `logo_clearbit_${domain.replace(/\./g, '_')}.png`;
  const dest = `${outputDir}/${filename}`;

  const result = await downloadFile(logoUrl, dest);

  return {
    source: 'Clearbit',
    success: result.success,
    path: result.path,
    url: logoUrl
  };
}

/**
 * 从 Google 获取 Favicon
 */
async function fetchGoogleFavicon(domain, outputDir) {
  const faviconUrl = `https://www.google.com/s2/favicons?domain=${domain}&sz=256`;
  const filename = `logo_google_favicon_${domain.replace(/\./g, '_')}.png`;
  const dest = `${outputDir}/${filename}`;

  const result = await downloadFile(faviconUrl, dest);

  return {
    source: 'Google',
    success: result.success,
    path: result.path,
    url: faviconUrl
  };
}

module.exports = {
  fetchClearbit,
  fetchGoogleFavicon
};
```

---

## 你想先实现哪个扩展？

1. **Clearbit Logo API** - 最快见效，1 行代码获取高清 Logo
2. **网站爬虫** - 更全面的站内素材发现
3. **图片质量评估** - 自动选择最佳版本
4. **全部实现** - 我会按优先级逐个完成
