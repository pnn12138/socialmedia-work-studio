# Image Finder Skill - Pexels API 调研文档

## 概述

Pexels 提供免费的高质量可商用图片素材，支持通过 API 进行搜索和获取。

---

## API 鉴权方式

- **认证方式**: API Key (Bearer Token)
- **请求头格式**: `Authorization: Bearer {YOUR_API_KEY}`
- **获取方式**: 在 https://www.pexels.com/api/ 注册账号后申请
- **安全要求**: API Key 需妥善保管，不应提交到公开代码仓库

---

## 主要接口

### 1. photos.search - 搜索图片

搜索 Pexels 图库中的图片。

**端点**: `GET https://api.pexels.com/v1/search`

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 搜索关键词 |
| orientation | string | 否 | 图片方向：portrait, landscape, square |
| size | string | 否 | 图片尺寸：small, medium, large |
| color | string | 否 | 主导颜色：red, orange, yellow, green, turquoise, blue, magenta, purple, pink, brown, black, gray, white, yellow-orange |
| per_page | number | 否 | 每页数量，默认 15，最大 80 |
| page | number | 否 | 页码，用于分页 |
| locale | string | 否 | 语言环境，默认 en-US |
| collection | string | 否 | 限定搜索特定合集 |
| filters | string | 否 | 过滤选项（如：color_filter） |

### 2. photos.curated - 精选图片

获取 Pexels 精选的图片。

**端点**: `GET https://api.pexels.com/v1/curated`

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orientation | string | 否 | portrait, landscape, square |
| size | string | 否 | small, medium, large |
| per_page | number | 否 | 默认 15，最大 80 |
| page | number | 否 | 页码 |
| locale | string | 否 | 语言环境 |

### 3. photos.show - 获取图片详情

通过图片 ID 获取单张图片的详细信息。

**端点**: `GET https://api.pexels.com/v1/photos/{id}`

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 图片 ID |

---

## 返回字段结构

### Search/Curated 响应

```json
{
  "page": 1,
  "per_page": 15,
  "photos": [
    {
      "id": 2014422,
      "width": 4000,
      "height": 6000,
      "url": "https://www.pexels.com/photo/photo-2014422/",
      "photographer": "John Doe",
      "photographer_url": "https://www.pexels.com/@johndoe",
      "photographer_id": 123456,
      "avg_color": "#8A7A6B",
      "src": {
        "original": "https://images.pexels.com/photos/2014422/pexels-photo-2014422.jpeg",
        "large2x": "https://images.pexels.com/photos/2014422/pexels-photo-2014422.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "large": "https://images.pexels.com/photos/2014422/pexels-photo-2014422.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "medium": "https://images.pexels.com/photos/2014422/pexels-photo-2014422.jpeg?auto=compress&cs=tinysrgb&h=350",
        "small": "https://images.pexels.com/photos/2014422/pexels-photo-2014422.jpeg?auto=compress&cs=tinysrgb&h=130",
        "portrait": "...",
        "landscape": "...",
        "tiny": "..."
      },
      "liked": false,
      "alt": "描述文本"
    }
  ],
  "total_results": 10000,
  "next_page": "https://api.pexels.com/v1/search?page=2&query=nature"
}
```

### Show 响应

返回单个 photo 对象，结构与上述 photos 数组中的元素相同。

---

## 速率限制

| 限制类型 | 数值 | 说明 |
|----------|------|------|
| 请求/小时 | 不限 | 但需合理使用 |
| 请求/天 | 建议 20000 | 超过可能需申请 |
| 并发限制 | 建议控制 | 避免短时间内大量请求 |

**注意事项**:
- 免费账户有足够的额度供日常使用
- 如需要更高限额，可联系 Pexels 申请
- 建议实现请求节流和缓存机制

---

## Attribution 要求

Pexels API 要求在使用图片时进行署名（Attribution）：

### 必须包含的信息

1. **摄影师姓名** (photographer)
2. **来源链接** (url 或 photographer_url)

### 署名格式示例

```
Photo by [摄影师姓名] from Pexels
链接到：https://www.pexels.com/photo/[photo-id]/
```

### 署名位置建议

- 社交媒体帖子：在图片说明或评论区注明
- 文章/博客：在图片下方或文末注明
- 视频：在描述或片尾注明

---

## 可用搜索参数字段汇总

| 字段 | 类型 | 可选值 |
|------|------|--------|
| query | string | 任意搜索词 |
| orientation | string | portrait, landscape, square |
| size | string | small, medium, large |
| color | string | red, orange, yellow, green, turquoise, blue, magenta, purple, pink, brown, black, gray, white, yellow-orange |
| per_page | number | 1-80 |
| page | number | 1+ |

---

## JavaScript SDK 使用方式

### 安装

```bash
npm install pexels
```

### 初始化

```javascript
const { createClient } = require('pexels');

const client = createClient('YOUR_API_KEY');
```

### 主要方法

```javascript
// 搜索图片
client.photos.search({ query: 'nature', orientation: 'landscape', per_page: 10 });

// 获取精选图片
client.photos.curated({ orientation: 'portrait', per_page: 10 });

// 获取图片详情
client.photos.show({ id: 2014422 });

// 随机图片
client.photos.random();
```

---

## 扩展考虑

未来扩展其他平台时需要注意：

1. **Unsplash**: 需要不同的鉴权方式（Client-ID 头）
2. **Pixabay**: 参数命名可能不同
3. **Freepik**: 部分资源需要付费授权
4. **统一归一化**: 需要将不同平台的返回格式转换为统一输出格式
