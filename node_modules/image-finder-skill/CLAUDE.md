# Image Finder - CLAUDE.md

此技能使用 Node.js 和 Pexels API 实现图片素材检索。

## 环境要求

- Node.js 16+
- npm
- Pexels API Key

## 安装依赖

```bash
cd .claude/skills/image-finder
npm install
```

## 配置 API Key

**推荐方式**：在项目根目录创建 `.env` 文件

```bash
# D:\social-work-flow\work-studio\.env
PEXELS_API_KEY=your_api_key_here
```

脚本会自动向上查找并加载根目录的 `.env` 文件，无需手动配置路径。

也可通过系统环境变量设置：

```bash
PEXELS_API_KEY=xxx node index.js
```

## 使用方式

### 方式 1：直接调用

```bash
node index.js
```

### 方式 2：测试脚本

```bash
node test.js "AI technology" --orientation=landscape --per_page=5
```

### 方式 3：在代码中引用

```javascript
const finder = require('./index');

const results = await finder.searchImages('AI technology', {
  orientation: 'landscape',
  per_page: 5
});

console.log(results);
```

## 输出格式

```json
{
  "source": "pexels",
  "query": "AI technology",
  "results": [
    {
      "id": "123456",
      "title": "Description",
      "photographer": "John Doe",
      "photographer_url": "https://...",
      "page_url": "https://...",
      "image_url": "https://...",
      "thumb_url": "https://...",
      "width": 1920,
      "height": 1080,
      "alt": "Description"
    }
  ]
}
```

## 扩展 Provider

添加新图片平台：

1. 在 `providers/` 创建新文件（如 `unsplash.js`）
2. 实现 `searchImages(query, options)` 方法
3. 返回标准化格式（使用 `utils/normalize.js`）
4. 在 `index.js` 中注册新 Provider

## 虚拟环境说明

本项目使用 uv 管理 Python 虚拟环境。

如需在 Python 环境中调用此技能，可通过子进程执行：

```python
import subprocess
import json

result = subprocess.run(
    ['node', 'index.js'],
    cwd='.claude/skills/image-finder',
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)
```
