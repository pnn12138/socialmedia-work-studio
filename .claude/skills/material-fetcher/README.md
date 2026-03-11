# 素材获取模块 (Material Fetcher) - 完成总结

## 模块结构

```
.claude/skills/material-fetcher/
├── CLAUDE.md                    # 模块说明（含扩展指南）
├── SKILL.md                     # 技能定义（统一入口）
├── index.js                     # 主入口/命令行解析
├── package.json                 # 依赖配置
├── test.js                      # 测试脚本
│
├── fetchers/                    # 各渠道 Fetcher
│   ├── github-fetcher.js        # GitHub 资源获取 ✅
│   ├── web-assets.js            # 官网品牌资产获取 ✅
│   ├── xhs-downloader.js        # 小红书图片下载 ⚪
│   └── logo-grabber.js          # Logo 聚合搜索 ✅
│
├── downloaders/                 # 下载器
│   └── universal.js             # 通用下载器 ✅
│
└── utils/                       # 工具函数
    └── url-extractor.js         # URL 提取工具 ✅
```

## 已完成功能

| 模块 | 状态 | 说明 |
|------|------|------|
| **GitHub Fetcher** | ✅ 完成 | 支持获取 Logo、README 图片、Releases Assets |
| **Web Assets Fetcher** | ✅ 完成 | 支持获取官网 Logo、favicon、OG Image |
| **Logo Grabber** | ✅ 完成 | 聚合 GitHub + 官网搜索 Logo |
| **Universal Downloader** | ✅ 完成 | 通用 HTTP 下载器 |
| **URL Extractor** | ✅ 完成 | 从 HTML 提取图片链接 |
| **XHS Downloader** | ⚪ 占位 | 需扩展 xiaohongshu-mcp 服务 |

## 使用方式

### 命令行执行

```bash
# 进入模块目录
cd .claude/skills/material-fetcher/

# 获取 GitHub 项目 Logo
node index.js github:petersteinberger/openclaw type:logo

# 获取官网品牌资产
node index.js web:https://example.com type:all

# 聚合搜索 Logo
node index.js logo:OpenClaw
```

### 通过技能调用

```
/material-fetcher github:petersteinberger/openclaw type:logo
```

### 在代码中调用

```javascript
const { fetchGitHub } = require('./fetchers/github-fetcher');
const { fetchLogo } = require('./fetchers/logo-grabber');

// 获取 GitHub 资源
const result = await fetchGitHub('petersteinberger/openclaw', 'logo', outputDir);

// 聚合搜索 Logo
const logoResult = await fetchLogo('OpenClaw', outputDir);
```

## 输出示例

```
[Material Fetcher] 开始获取...
  源：github
  标识符：petersteinberger/openclaw
  输出目录：/path/to/fig/素材

[Material Fetcher] 获取完成！

获取到的文件：
  1. [logo] logo_petersteinberger_openclaw_logo.svg
     路径：/path/to/fig/素材/logo_petersteinberger_openclaw_logo.svg
  2. [readme_image] readme_petersteinberger_openclaw_1710064800.jpg
     路径：/path/to/fig/素材/readme_petersteinberger_openclaw_1710064800.jpg
```

## 小红书下载扩展指南

### 当前限制

`xiaohongshu-mcp` 服务的 `get_feed_detail` 可以获取笔记详情（包含图片 URL），但没有提供下载工具。

### 实现步骤

1. **扩展 xiaohongshu-mcp 服务**

   在 `xiaohongshu-mcp` 服务中添加 `download_images` 工具：

   ```go
   func download_images(params map[string]interface{}) ([]interface{}, error) {
       // 1. 获取笔记详情
       detail, err := getFeedDetail(params["feed_id"], params["xsec_token"])

       // 2. 下载图片
       for _, imgUrl := range detail.Images {
           downloadFile(imgUrl, params["output_dir"])
       }
   }
   ```

2. **创建对应的 Skill**

   在 `.claude/skills/xiaohongshu-mcp-skills/skills/xhs-downloader/` 创建 `SKILL.md`

3. **启用 XHS Downloader**

   修改 `fetchers/xhs-downloader.js` 中的 `getFeedDetail` 函数，调用 MCP 服务

### 参考文档

详见 `CLAUDE.md` 中的「附录：小红书 MCP 扩展指南」

## 版权与合规

| 来源 | 商用许可 | 署名要求 | 风险等级 |
|------|----------|----------|----------|
| GitHub 项目资产 | 需查看项目 LICENSE | 建议署名 | 中 |
| 官网 Logo | 需查看品牌规范 | 通常需要 | 中 |
| 小红书笔记图片 | **原作者版权** | 必须授权 | 高 |
| Pexels/Unsplash | 免费商用 | 建议署名 | 低 |

**使用原则**：
1. 小红书图片仅用于学习参考，不直接商用
2. 品牌 Logo 用于评论/分析类内容属于合理使用
3. 优先使用官方渠道和开源项目资产
4. 商用内容必须验证授权

## 下一步行动

### 立即可用

- ✅ 使用 `material-fetcher` 获取 OpenClaw Logo

### 可选扩展

1. **测试 GitHub Fetcher**

   运行测试脚本验证功能：
   ```bash
   node test.js
   ```

2. **扩展小红书下载能力**

   参考上述「小红书下载扩展指南」实现完整功能

3. **添加更多渠道**

   - Twitter/X 图片下载
   - Instagram 图片下载
   - Pinterest 图片下载

## 文件清单

| 文件 | 行数 | 说明 |
|------|------|------|
| `CLAUDE.md` | ~120 | 模块说明与扩展指南 |
| `SKILL.md` | ~80 | 技能定义与使用规范 |
| `index.js` | ~150 | 主入口与命令行解析 |
| `github-fetcher.js` | ~180 | GitHub 资源获取 |
| `web-assets.js` | ~150 | 官网品牌资产获取 |
| `logo-grabber.js` | ~100 | Logo 聚合搜索 |
| `xhs-downloader.js` | ~100 | 小红书下载器（占位） |
| `universal.js` | ~120 | 通用下载器 |
| `url-extractor.js` | ~100 | URL 提取工具 |

**总计**：~1100 行代码
