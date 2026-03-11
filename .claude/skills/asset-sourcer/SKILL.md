# Asset Sourcer - 素材获取技能

## 技能描述

素材补充能力技能，负责获取外部素材供 image-card-builder 使用。此技能不应默认参与所有图片生成，只处理外部素材需求。

整合了 image-finder、material-fetcher、web-screenshot-capture 的能力，提供统一的素材获取接口。

## 快速开始

```bash
# 从 visual_plan.md 获取素材需求
/asset-sourcer {topic-name} --plan topics/{topic-name}/fig/visual_plan.md

# 搜索特定素材
/asset-sourcer --query "AI technology background" --type background --orientation portrait

# 获取品牌 Logo
/asset-sourcer --brand openclaw --type logo

# 截取网页截图
/asset-sourcer --screenshot https://example.com --output fig/素材/screenshot.png
```

## 职责范围

此技能负责：

1. 通过素材 API 搜索背景图或配图
2. 下载图标、Logo
3. 用浏览器脚本截取网页局部
4. 将所有素材统一存入 `fig/素材/`
5. 输出 `assets.json` 或更新后的 spec

此技能**不负责**：
- 直接渲染最终图片
- 决定图片的视觉风格
- 替代 image-card-builder

## 素材获取时机

只有以下情况才使用此技能：

1. 需要真实照片背景
2. 需要产品官网截图
3. 需要某个开源项目页面的界面截图
4. 需要某品牌或工具 logo
5. 需要一张科技背景底图增强封面表现力

## 输入来源

默认按以下优先级读取：

1. `topics/{topic-name}/fig/visual_plan.md` - 素材需求清单
2. `topics/{topic-name}/fig/specs/*.json` - 单张 spec 中的 asset_needs
3. 用户直接输入的素材需求

## 输出文件

在 `topics/{topic-name}/fig/` 下生成：

```
topics/{topic-name}/fig/
├── 素材/
│   ├── logo_openclaw.svg
│   ├── bg_tech_01.jpg
│   ├── screenshot_dashboard.png
│   └── ...
├── assets.json           # 素材清单
└── search-results.md     # 搜索结果记录
```

## 素材来源

### P0 - 必执行

| 平台 | 说明 | 超时设置 |
|------|------|----------|
| GitHub | 项目仓库 | 30s |
| 官网首页 | 解析 favicon/meta | 30s |
| Clearbit | Logo API | 15s |
| Google Favicon | favicon 服务 | 15s |
| Pexels | 图片/视频搜索 | 30s |

### P1 - 条件执行

当 P0 未找到 SVG 或高质量素材时执行：

| 平台 | 说明 | 超时设置 |
|------|------|----------|
| 官网子页面 | /brand, /press, /media | 60s |
| Brandfetch | 品牌 API | 30s |
| Unsplash | 高质量图片 | 30s |

### P2 - 备选方案

当前面都失败时执行：

| 平台 | 说明 | 超时设置 |
|------|------|----------|
| DuckDuckGo Images | 图片搜索 | 30s |
| Bing Images | 图片搜索 | 30s |

## 素材类型

| 类型 | 说明 | 获取方式 |
|------|------|----------|
| `logo` | 品牌 Logo | material-fetcher, Clearbit |
| `icon` | 图标元素 | SVG 绘制，图标库 |
| `background` | 背景图 | Pexels, Unsplash |
| `screenshot` | 网页截图 | web-screenshot-capture |
| `product` | 产品图 | 官网，GitHub |
| `texture` | 纹理底图 | Pexels, 图案库 |

## 工作流程

```
读取 visual_plan.md -> 解析 asset_needs -> 选择获取方式 -> 下载素材
                                                    ↓
                                            保存至 fig/素材/
                                                    ↓
                                            更新 assets.json
                                                    ↓
                                            通知 visual-planner
```

## 使用示例

### 示例 1：从 visual_plan.md 获取素材需求

```bash
/asset-sourcer openclaw-analysis --plan topics/openclaw-analysis/fig/visual_plan.md
```

### 示例 2：搜索背景图

```bash
/asset-sourcer --query "technology background blue" --type background --orientation portrait --per_page 10
```

### 示例 3：获取品牌 Logo

```bash
/asset-sourcer --brand openclaw --type logo --output fig/素材/
```

### 示例 4：截取网页

```bash
/asset-sourcer --screenshot https://github.com/openclaw/openclaw --output fig/素材/github.png
```

## 素材质量标准

### Logo 质量标准

| 等级 | 格式 | 分辨率 | 说明 |
|------|------|--------|------|
| **S** | SVG | 任意 | 最佳 - 可无限缩放 |
| **A** | PNG | ≥512x512 | 优秀 - 高分辨率 |
| **B** | PNG | ≥256x256 | 良好 - 可用 |
| **C** | PNG/JPG | ≥128x128 | 勉强可用 |
| **D** | 任意 | <128x128 | 不推荐，需人工替换 |

### 背景图质量标准

| 等级 | 分辨率 | 说明 |
|------|--------|------|
| **S** | ≥4K | 最佳 - 可任意裁剪 |
| **A** | ≥1920x1080 | 优秀 - 高清 |
| **B** | ≥1280x720 | 良好 - 可用 |
| **C** | ≥640x480 | 勉强可用 |
| **D** | <640x480 | 不推荐，需人工替换 |

### 评分公式

```
质量分 = 格式分 + 分辨率分 + 附加分

格式分:
- SVG: 100
- PNG: 80
- WEBP: 70
- JPG: 50
- ICO: 30

分辨率分:
- ≥512px: 40
- ≥256px: 30
- ≥128px: 20
- <128px: 10

附加分:
- 透明背景：+20
- 文件<50KB: +10
- 官方来源：+10
```

## 文件命名规范

```
格式：<type>_<source>_<identifier>[_<version>].<ext>

type:
- logo: Logo 文件
- icon: 图标文件
- background: 背景图
- screenshot: 截图
- texture: 纹理
- product: 产品图

source:
- github: GitHub
- clearbit: Clearbit API
- google: Google Favicon
- brandfetch: Brandfetch
- pexels: Pexels
- unsplash: Unsplash
- official: 官网
```

**示例**：
- `logo_clearbit_openclaw.png`
- `logo_github_openclaw.svg`
- `background_pexels_tech_01.jpg`
- `screenshot_official_dashboard.png`

## 与其他技能协作

| 技能 | 协作内容 |
|------|----------|
| `visual-planner` | 接收素材需求清单 |
| `image-finder` | 搜索 Pexels 图片 |
| `material-fetcher` | 获取品牌资产、Logo |
| `web-screenshot-capture` | 网页截图 |
| `image-card-builder` | 提供素材供渲染 |
| `background-remover` | 去背景处理 |

## assets.json 格式

```json
{
  "topic": "openclaw-analysis",
  "generated_at": "2026-03-10T12:00:00",
  "assets": [
    {
      "id": "logo-01",
      "type": "logo",
      "filename": "logo_clearbit_openclaw.png",
      "source": "clearbit",
      "url": "https://logo.clearbit.com/openclaw.com",
      "format": "png",
      "resolution": "512x512",
      "quality_score": 90,
      "status": "success",
      "notes": "官方 Logo，高清"
    },
    {
      "id": "bg-01",
      "type": "background",
      "filename": "background_pexels_tech_01.jpg",
      "source": "pexels",
      "photographer": "John Doe",
      "format": "jpg",
      "resolution": "1920x1080",
      "quality_score": 85,
      "status": "success",
      "notes": "科技背景，适合封面"
    }
  ]
}
```

## 搜索参数

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `query` | 搜索关键词 | 任意文本 |
| `type` | 素材类型 | logo, background, icon, texture |
| `orientation` | 图片方向 | portrait, landscape, square |
| `color` | 主导颜色 | red, orange, yellow, green, blue, etc. |
| `size` | 图片尺寸 | small, medium, large |
| `per_page` | 返回数量 | 1-80 |
| `page` | 页码 | 1+ |

## 版权与合规

### 可使用素材

| 来源 | 商用 | 署名 | 说明 |
|------|------|------|------|
| GitHub 开源项目 | ✅ | 建议 | 遵循项目 LICENSE |
| 官网品牌资产 | ✅ | 通常需要 | 评论/分析属合理使用 |
| Clearbit Logo API | ✅ | 否 | 聚合公开数据 |
| Google Favicon | ✅ | 否 | 公开服务 |
| Pexels | ✅ | 否 | 免费商用 |
| Unsplash | ✅ | 否 | 免费商用 |

### 限制使用素材

| 来源 | 限制 | 说明 |
|------|------|------|
| 小红书笔记图片 | ❌ 商用 | 仅学习参考 |
| 第三方图库 | 需验证 | 检查授权条款 |
| 品牌官方素材 | 需谨慎 | 避免商标侵权 |

## 错误处理

| 错误 | 处理方式 |
|------|----------|
| API Key 缺失 | 提示用户配置环境变量 |
| 素材不存在 | 尝试备选来源，或标记人工搜索 |
| 下载失败 | 重试 2 次，失败则报错 |
| 质量不达标 | 尝试更高清来源，或提示人工替换 |
| 版权不明 | 标记需谨慎使用 |

## 环境要求

- Node.js 16+ 或 Python 3.8+
- Pexels API Key（环境变量 `PEXELS_API_KEY`）
- 访问网络和外部 API 的权限

## 环境变量配置

在项目根目录创建 `.env` 文件：

```bash
# Pexels API
PEXELS_API_KEY=your_api_key

# Unsplash API（可选）
UNSPLASH_ACCESS_KEY=your_key

# Pixabay API（可选）
PIXABAY_API_KEY=your_key
```

## 最佳实践

1. **先读 visual_plan.md** - 理解素材需求
2. **优先高质量来源** - SVG > 高清 PNG > 普通图片
3. **记录来源信息** - 便于追溯和版权确认
4. **统一文件命名** - 便于管理和查找
5. **及时更新 assets.json** - 让其他技能知道素材状态
6. **质量不达标时提示** - 不要勉强使用低质素材

## 迭代机制

当素材质量不达标或找不到时：

```
评估素材 → 不足则输出补充清单 → 人工补充 → 重新评估 → 循环直到足够
```

**素材足够的标准**：
- 核心素材（Logo、关键截图）质量分≥80
- 每张图都有对应的素材支撑
- 无关键素材缺失
