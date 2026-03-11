# Web Screenshot Capture - 网页/界面截图技能

## 技能描述

此技能负责网页、界面、软件窗口的截图捕获，支持全屏、局部、重点区域保留与基础标注。

## 用途

- 截取网页内容作为素材
- 捕获软件界面、对话框、错误提示
- 截取代码编辑器、终端窗口
- 截取社交媒体、新闻页面
- 为技术文章提供界面证据

## 适用场景

| 场景 | 说明 |
|------|------|
| 技术教程 | 截取软件界面、操作步骤 |
| 安全分析 | 截取漏洞演示、警告页面 |
| 产品评测 | 截取 UI 界面、功能展示 |
| 数据引用 | 截取图表、数据页面 |
| 对比图制作 | 截取前后对比、版本差异 |

## 输入参数

```markdown
- **target**: 截图目标（URL、窗口名称、应用名称）
- **mode**: 截图模式
  - `full` - 全屏/整页
  - `visible` - 可视区域
  - `element` - 指定元素/CSS 选择器
  - `region` - 指定坐标区域
- **annotations**: 标注需求（可选）
  - 箭头、圆圈、高亮框
  - 文字说明、编号标记
  - 模糊/马赛克处理
- **output_name**: 输出文件名（可选）
- **post_process**: 后处理要求（可选）
  - 裁剪、缩放
  - 去干扰元素（广告、导航栏）
  - 格式转换
```

## 输出

```
topics/{topic-name}/fig/原始素材/
├── screenshot_{target}_{timestamp}.png    # 原始截图
└── screenshot_{target}_{timestamp}_edited.png  # 标注后版本（如有）
```

## 执行步骤

### 方式一：网页截图（URL 目标）

1. 打开目标 URL
2. 根据 `mode` 执行截图：
   - `full` - 滚动截长图，捕获整个页面
   - `visible` - 捕获当前视口
   - `element` - 定位并捕获指定元素
3. 保存为 PNG 格式
4. 如有 `annotations`，添加标注
5. 存入 `原始素材/` 目录

### 方式二：窗口/应用截图

1. 定位目标窗口或应用
2. 捕获窗口内容
3. 可选：去除窗口装饰（标题栏、边框）
4. 保存并命名

### 方式三：用户手动截屏指引

当自动截图不可用时，输出清晰的截屏指引：

```markdown
## 截屏指引

请截取以下内容：

1. **目标**: [描述要截取的内容]
2. **位置**: [URL 或 应用名称]
3. **范围**: [全屏/局部/特定区域]
4. **要求**:
   - 分辨率不低于 1920x1080
   - 确保内容清晰可读
   - 避免无关元素入镜
5. **保存为**: `{output_name}`
```

## 失败时的兜底策略

| 失败原因 | 兜底方案 |
|----------|----------|
| URL 无法访问 | 告知用户，请求替代 URL 或手动截图 |
| 目标应用未运行 | 告知用户启动应用后重试 |
| 权限不足（如 macOS 录屏权限） | 输出权限配置指引，切换到手动截屏模式 |
| 动态内容加载失败 | 增加等待时间后重试，或告知用户手动操作 |

## 推荐后端实现

### 方式一：CLI 工具（推荐）

```bash
# macOS - screencapture
screencapture -x output.png

# Linux - flameshot/scrot
flameshot gui -p output.png

# Windows - PowerShell
Add-Type -AssemblyName System.Windows.Forms
$form = New-Object System.Windows.Forms.Form
$form.TopMost = $true
$graphics = [System.Drawing.Graphics]::FromHwnd($form.Handle)
$bmp = New-Object System.Drawing.Bitmap 1920,1080
$graphics.CopyFromScreen(0,0,0,0,$bmp.Size)
$bmp.Save("output.png")
```

### 方式二：Node.js + Puppeteer（网页截图）

```javascript
const puppeteer = require('puppeteer');

async function capturePage(url, outputPath) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle2' });
  await page.screenshot({ path: outputPath, fullPage: true });
  await browser.close();
}
```

### 方式三：Python + Selenium/Playwright

```python
from playwright.sync_api import sync_playwright

def capture_page(url, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=output_path, full_page=True)
        browser.close()
```

### 方式四：MCP Server 接入

如项目配置了 MCP，可接入 `screenshot-mcp` 或 `browser-mcp`：

```json
{
  "mcpServers": {
    "screenshot": {
      "command": "npx",
      "args": ["-y", "screenshot-mcp"]
    }
  }
}
```

## 标注功能说明

基础标注支持：

- **高亮框**: 矩形框选重点区域
- **箭头**: 指向特定元素
- **圆圈**: 圈出关键信息
- **文字**: 添加简短说明
- **编号**: 多步骤操作标记
- **模糊**: 隐藏敏感信息

标注应简洁、不遮挡核心内容、颜色与背景形成对比。

## 与 post-builder 的交接

- 截图完成后存入 `原始素材/`
- 在 `build-log.md` 中记录截图来源、时间、模式
- 如有标注，说明标注内容和位置
- 交由 `image-compose-local` 进行二次处理（如需要）

## 文件命名规范

```
screenshot_{target}_{YYYYMMDD}_{sequence}.png

示例：
screenshot_github-home_20260309_01.png
screenshot_error-dialog_20260309_01.png
screenshot_dashboard-chart_20260309_01.png
```
