# Image Compose Local - 本地图像合成与编辑技能

## 技能描述

此技能负责本地图像的裁剪、缩放、拼接、加字、叠图、信息卡制作等二次编辑工作，是将原始素材转化为高完成度定稿图的核心工具。

## 快速开始

### 基础用法

```bash
# 调用技能
/image-compose-local <input_image> -o <output_path> [options]
```

### 常用命令

```bash
# 裁剪至 3:4 比例
/image-compose-local input.jpg -o output.jpg --ratio 3:4

# 缩放至指定宽度
/image-compose-local input.jpg -o output.jpg --width 1080

# 添加文字
/image-compose-local input.jpg -o output.jpg --text "标题文字"

# 创建引用卡片
/image-compose-local bg.jpg -o quote.png --quote "这是一句引用" --author "作者"

# 创建对比图
/image-compose-local before.jpg -o compare.png --compare "after.jpg:Before:After"

# 执行复杂操作（JSON）
/image-compose-local input.jpg -o output.jpg --operations '{"operations": [...]}'
```

## 环境要求

- Python 3.8+
- Pillow (`pip install pillow`)

## 安装依赖

```bash
cd .claude/skills/image-compose-local
pip install pillow
```

## 用途

- 裁剪图片至目标比例
- 调整图片分辨率与尺寸
- 多图拼接（横向、纵向、网格）
- 添加文字标题、标签、说明
- 图层叠加与混合
- 制作信息卡片、对比图
- 调整色调、亮度、对比度
- 添加边框、装饰元素

## 适用场景

| 场景 | 说明 | 命令示例 |
|------|------|----------|
| 封面制作 | 裁剪至 3:4 比例，添加标题区留白 | `--ratio 3:4 --text "标题"` |
| 信息图 | 多图拼接 + 文字说明 | `--operations '[{"type":"compose"}]'` |
| 对比图 | 左右/上下对比布局 | `--compare "after.jpg:Before:After"` |
| 引用卡片 | 文字 + 背景 + 署名 | `--quote "引用" --author "作者"` |
| 批量调整 | 统一色调、尺寸 | `--operations '[{"type":"adjust"}]'` |

## 输入参数

### 命令行参数

```bash
# 必需参数
<input>              # 源图片路径
-o, --output         # 输出文件路径

# 快捷参数
--ratio              # 裁剪比例，如 "3:4", "16:9", "1:1"
--width              # 目标宽度（像素）
--height             # 目标高度（像素）
--text               # 添加文字内容
--style              # 风格预设（minimalist/tech-dark/business/warning/cute-tech）
--quote              # 引用文字（创建引用卡片时使用）
--author             # 作者（引用卡片时使用）
--compare            # 对比图，格式："image2_path:label1:label2"

# 高级参数（JSON 操作）
--operations         # JSON 字符串或文件路径，定义复杂操作序列
```

### JSON 操作格式

```json
{
  "operations": [
    {
      "type": "crop",
      "ratio": "3:4",
      "focus": "center"
    },
    {
      "type": "resize",
      "width": 1080,
      "height": 1440,
      "mode": "lanczos"
    },
    {
      "type": "text",
      "content": "标题文字",
      "position": {"anchor": "top-center"},
      "size": 48,
      "color": "#FFFFFF",
      "offset": [0, 50]
    },
    {
      "type": "adjust",
      "brightness": 1.1,
      "contrast": 1.05,
      "saturation": 1.0
    },
    {
      "type": "border",
      "width": 20,
      "color": "#FFFFFF",
      "radius": 10
    }
  ]
}
```

### 操作类型详解

| 操作类型 | 参数 | 说明 |
|----------|------|------|
| `crop` | `ratio`, `focus` | 按比例裁剪，focus 为中心/上/下/左/右 |
| `resize` | `width`, `height`, `mode` | 缩放图片，mode 为缩放算法 |
| `text` | `content`, `position`, `size`, `color` | 添加单行文字 |
| `compose` | `layout`, `gap`, `background` | 多图拼接 |
| `overlay` | `image`, `position`, `opacity` | 叠加图层 |
| `adjust` | `brightness`, `contrast`, `saturation` | 颜色调整 |
| `border` | `width`, `color`, `radius` | 添加边框 |

## 输出

```
topics/{topic-name}/fig/定稿图/
├── 01_cover.png           # 封面定稿
├── 02_inner_01.png        # 内页 1 定稿
├── 03_inner_02.png        # 内页 2 定稿
└── ...
```

## 风格预设

| 预设名称 | 背景色 | 主色 | 辅色 | 强调色 | 适用场景 |
|----------|--------|------|------|--------|----------|
| `minimalist` | #FFFFFF | #000000 | #666666 | #333333 | 引用卡片、金句图 |
| `tech-dark` | #0D0D0D | #FFFFFF | #A0A0A0 | #2563EB | 技术文章封面、架构 |
| `business` | #F0F4F8 | #1E3A5F | #5A7A9A | #2E5C8A | 报告、数据图 |
| `warning` | #FEF3C7 | #92400E | #B45309 | #DC2626 | 安全警示、风险提示 |
| `cute-tech` | #FFF5F5 | #4A154B | #7C3AED | #EC4899 | 可爱科技风、轻松主题 |

## 使用示例

### 1. 裁剪图片

```bash
# 裁剪为 3:4 比例（小红书封面）
/image-compose-local input.jpg -o output.jpg --ratio 3:4

# 裁剪为 16:9 比例（横版封面）
/image-compose-local input.jpg -o output.jpg --ratio 16:9

# 裁剪并聚焦于上方
/image-compose-local input.jpg -o output.jpg --ratio 3:4 --focus top
```

### 2. 缩放图片

```bash
# 缩放到指定宽度
/image-compose-local input.jpg -o output.jpg --width 1080

# 缩放到指定尺寸
/image-compose-local input.jpg -o output.jpg --width 1080 --height 1440
```

### 3. 添加文字

```bash
# 添加居中文字
/image-compose-local input.jpg -o output.jpg --text "标题文字"

# 使用 JSON 定义复杂文字效果
/image-compose-local input.jpg -o output.jpg --operations '{
  "operations": [{
    "type": "text",
    "content": "多行文字\\n第二行",
    "position": {"anchor": "center"},
    "size": 48,
    "color": "#FFFFFF"
  }]
}'
```

### 4. 创建引用卡片

```bash
# 简单引用卡片
/image-compose-local bg.jpg -o quote.png --quote "这是一句引用" --author "作者名"

# 使用风格预设
/image-compose-local bg.jpg -o quote.png --quote "科技改变世界" --author "乔布斯" --style tech-dark
```

### 5. 创建对比图

```bash
# 左右对比
/image-compose-local before.jpg -o compare.png --compare "after.jpg:Before:After"

# 上下对比
/image-compose-local before.jpg -o compare.png --compare "after.jpg:Before:After:vertical"
```

### 6. 复杂操作序列

```bash
# 裁剪 -> 缩放 -> 加字 -> 调色
/image-compose-local input.jpg -o output.jpg --operations '{
  "operations": [
    {"type": "crop", "ratio": "3:4"},
    {"type": "resize", "width": 1080, "height": 1440},
    {"type": "text", "content": "标题", "size": 48, "color": "#FFFFFF"},
    {"type": "adjust", "brightness": 1.1, "contrast": 1.05}
  ]
}'
```

## 失败时的兜底策略

| 失败原因 | 兜底方案 |
|----------|----------|
| 字体文件缺失 | 使用系统默认字体（Arial, 微软雅黑，思源黑体） |
| 图片分辨率过低 | 告知用户，尝试 upscale 或建议更换素材 |
| 颜色配置冲突 | 使用预设配色方案 |
| 复杂布局无法实现 | 简化为近似的简单布局，并说明差异 |
| Pillow 未安装 | 提示用户运行 `pip install pillow` |
| 输出路径无权限 | 尝试创建目录，失败则输出到当前目录 |

## Python 实现

本技能使用 Python + Pillow 实现，核心功能包括：

```python
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# 主要功能模块
# - crop_to_ratio(): 按比例裁剪
# - resize_image(): 缩放图片
# - add_text(): 添加文字
# - add_multiline_text(): 添加多行文字（自动换行）
# - compose_images(): 多图拼接
# - add_border(): 添加边框
# - adjust_colors(): 调整颜色
# - add_overlay(): 叠加图层
# - create_quote_card(): 创建引用卡片
# - compare_images(): 创建对比图
```

## 与 post-builder 的交接

- 接收来自 `原始素材/` 的图片
- 按 `requirements.md` 中的 `post_process_plan` 执行
- 输出至 `定稿图/`
- 在 `build-log.md` 中记录：
  - 使用的操作
  - 参数设置
  - 风格选择理由

## 文件命名规范

与 `定稿图/` 目录保持一致：

```
01_cover.png
02_inner_01.png
03_inner_02.png
04_inner_03.png
05_inner_04.png
```
