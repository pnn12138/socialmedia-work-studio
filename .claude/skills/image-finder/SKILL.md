# Image Finder 技能

## 技能描述

为 AI 内容生成系统自动检索可商用图片素材的技能。

支持多平台图片搜索（Pexels、Unsplash、Pixabay 等），提供统一的检索接口和标准化的输出格式。

## 使用方式

### 基础搜索

```
/image-finder [搜索关键词]
```

### 带参数搜索

```
/image-finder [搜索关键词] --orientation=portrait --per_page=10
```

### 参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| query | 搜索关键词（必填） | 任意文本 |
| orientation | 图片方向 | portrait, landscape, square |
| color | 主导颜色 | red, orange, yellow, green, blue, purple, pink, brown, black, gray, white |
| size | 图片尺寸 | small, medium, large |
| per_page | 返回数量 | 1-80 |
| page | 页码 | 1+ |

### 输出

返回 Top N 张图片的详细信息，包括：

- 图片 ID
- 标题和描述
- 摄影师信息
- 原图和缩略图链接
- 尺寸信息
- 署名信息

## 完整流程

```
用户请求 → index.js → provider选择 → API调用 → normalize格式化 → 返回结果
```

## 扩展能力

当前支持的 Provider：

- `pexels` - Pexels API（已实现）

计划支持：

- `unsplash` - Unsplash API
- `pixabay` - Pixabay API
- `freepik` - Freepik API
- `local` - 自建图库

## 与其他 Agent 协作

此技能可被以下 Agent 调用：

- `visual-planner` - 为视觉规划提供素材
- `post-builder` - 为内容组装提供图片
- `canonical-writer` - 为母稿配图

## 注意事项

1. **API Key 配置**: 需要在环境变量中设置 `PEXELS_API_KEY`
2. **Attribution**: 使用图片时需要按平台要求进行署名
3. **商用授权**: Pexels 图片可免费商用，但仍需注意肖像权等限制
4. **速率限制**: 建议实现缓存和节流机制

## 配置环境变量

在项目根目录创建 `.env` 文件：

```
PEXELS_API_KEY=your_api_key_here
```

或在调用时传入：

```bash
PEXELS_API_KEY=xxx node index.js
```
