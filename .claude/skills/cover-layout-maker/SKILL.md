# Cover Layout Maker - 封面排版制作技能

## 技能描述

此技能专门负责封面图的排版制作，包括标题区留白、标签条设计、封面模板应用、统一风格输出，是打造平台感封面的核心工具。

## 用途

- 为封面图添加标题区留白
- 制作统一风格的标签条/分类标识
- 应用封面模板（系列内容统一视觉）
- 调整封面图的视觉层级
- 确保封面文字清晰可读
- 输出符合平台尺寸要求的封面

## 适用场景

| 场景 | 说明 |
|------|------|
| 系列内容 | 统一封面模板，建立品牌感 |
| 技术文章 | 标题 + 副标题 + 标签 |
| 评测内容 | 评分标签 + 关键参数 |
| 教程内容 | 步骤编号 + 难度标签 |
| 盘点内容 | 数字突出 + 分类标签 |

## 输入参数

```markdown
- **source**: 源图片路径（背景图）
- **title**: 主标题内容
- **subtitle**: 副标题内容（可选）
- **tags**: 标签列表（可选）
  - 如：["AI 安全", "技术科普", "深度分析"]
- **layout_preset**: 布局预设
  - `top-title`: 标题在顶部
  - `bottom-title`: 标题在底部
  - `center-title`: 标题居中
  - `split`: 左右分割布局
- **style_preset**: 风格预设
  - `minimalist`: 极简风
  - `tech-dark`: 暗黑科技风
  - `business`: 商务风
  - `warning`: 警示风
- **output_ratio**: 目标比例
  - `3:4`: 小红书标准
  - `1:1`: 正方形
  - `16:9`: 横版
- **output_name**: 输出文件名
```

## 输出

```
topics/{topic-name}/fig/定稿图/
├── 01_cover.png    # 封面定稿
```

## 执行步骤

### 1. 标题区留白处理

```python
def add_title_spacing(image, position="bottom", spacing_ratio=0.25):
    """
    为标题添加留白区域
    position: "top", "bottom", "overlay"
    spacing_ratio: 留白区域占整体高度的比例
    """
    w, h = image.size

    if position == "bottom":
        # 底部扩展留白区
        new_h = int(h / (1 - spacing_ratio))
        spacing_h = new_h - h

        # 创建渐变背景
        from PIL import ImageDraw
        result = Image.new("RGB", (w, new_h), "#FFFFFF")
        result.paste(image, (0, 0))

        # 在留白区添加渐变遮罩
        draw = ImageDraw.Draw(result)
        for i in range(spacing_h):
            alpha = int(255 * (i / spacing_h))
            draw.rectangle(
                [0, h + i, w, h + i + 1],
                fill=(0, 0, 0, alpha)
            )

        return result

    elif position == "overlay":
        # 在图像底部添加半透明遮罩
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # 渐变遮罩
        gradient_h = int(h * 0.4)
        for i in range(gradient_h):
            alpha = int(180 * (i / gradient_h))
            y = h - gradient_h + i
            draw.rectangle([0, y, w, y + 1], fill=(0, 0, 0, alpha))

        return Image.alpha_composite(image.convert("RGBA"), overlay)
```

### 2. 标题文字排版

```python
def add_title_layout(image, title, subtitle=None, position="bottom"):
    """
    添加标题排版
    """
    draw = ImageDraw.Draw(image)
    w, h = image.size

    # 加载字体
    title_font = ImageFont.truetype("fonts/NotoSansSC-Bold.ttf", 48)
    subtitle_font = ImageFont.truetype("fonts/NotoSansSC-Regular.ttf", 24)

    # 计算位置
    if position == "bottom":
        title_y = h - int(h * 0.15)
        subtitle_y = h - int(h * 0.08)
    elif position == "top":
        title_y = int(h * 0.1)
        subtitle_y = int(h * 0.18)
    else:  # center
        title_y = h // 2 - 40
        subtitle_y = h // 2 + 20

    # 计算居中位置
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (w - title_w) // 2

    # 绘制标题（带描边增强对比度）
    outline_color = (0, 0, 0)
    text_color = (255, 255, 255)

    # 描边效果
    for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
        draw.text((title_x + dx, title_y + dy), title,
                  font=title_font, fill=outline_color)

    # 主文字
    draw.text((title_x, title_y), title, font=title_font, fill=text_color)

    # 副标题
    if subtitle:
        sub_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_x = (w - sub_w) // 2
        draw.text((sub_x, subtitle_y), subtitle,
                  font=subtitle_font, fill=text_color)

    return image
```

### 3. 标签条制作

```python
def add_tags(image, tags, position="top-left"):
    """
    添加分类标签条
    """
    draw = ImageDraw.Draw(image)
    w, h = image.size

    # 标签样式配置
    tag_bg = (255, 87, 34)  # 橙色背景
    tag_text = (255, 255, 255)  # 白色文字
    tag_font = ImageFont.truetype("fonts/NotoSansSC-Bold.ttf", 16)
    tag_padding = 12
    tag_gap = 8

    # 计算起始位置
    if position == "top-left":
        x_start = 16
        y_start = 16
    elif position == "top-right":
        x_start = w - 16
        y_start = 16
    else:
        x_start = 16
        y_start = h - 16 - len(tags) * (36 + tag_gap)

    for i, tag in enumerate(tags[:3]):  # 最多 3 个标签
        # 计算标签文字宽度
        bbox = draw.textbbox((0, 0), tag, font=tag_font)
        tag_w = bbox[2] - bbox[0] + tag_padding * 2
        tag_h = 36

        # 计算位置
        if position in ["top-left", "top-right"]:
            x = x_start + (i * (tag_w + tag_gap))
            y = y_start
        else:
            x = x_start
            y = y_start + (i * (tag_h + tag_gap))

        # 绘制标签背景（圆角矩形）
        tag_bg_layer = Image.new("RGBA", (tag_w, tag_h), (0, 0, 0, 0))
        tag_draw = ImageDraw.Draw(tag_bg_layer)
        tag_draw.rounded_rectangle(
            [0, 0, tag_w, tag_h],
            radius=6,
            fill=(*tag_bg, 200)
        )
        image.paste(tag_bg_layer, (x, y), tag_bg_layer)

        # 绘制标签文字
        draw.text((x + tag_padding, y + 10), tag,
                  font=tag_font, fill=tag_text)

    return image
```

### 4. 封面模板应用

```python
TEMPLATE_CONFIGS = {
    "tech-dark": {
        "bg_overlay": (0, 0, 0, 128),
        "title_color": (255, 255, 255),
        "accent_color": (33, 150, 243),  # 科技蓝
        "font_title": "NotoSansSC-Bold",
        "font_subtitle": "NotoSansSC-Regular",
        "title_position": "bottom",
    },
    "warning": {
        "bg_overlay": (0, 0, 0, 100),
        "title_color": (255, 235, 59),  # 警示黄
        "accent_color": (244, 67, 54),  # 警告红
        "font_title": "NotoSansSC-Black",
        "font_subtitle": "NotoSansSC-Bold",
        "title_position": "center",
    },
    "minimalist": {
        "bg_overlay": (255, 255, 255, 50),
        "title_color": (33, 33, 33),
        "accent_color": (100, 100, 100),
        "font_title": "NotoSansSC-Bold",
        "font_subtitle": "NotoSansSC-Light",
        "title_position": "center",
    },
}

def apply_cover_template(image, template_name, title, subtitle=None, tags=None):
    """
    应用封面模板
    """
    config = TEMPLATE_CONFIGS.get(template_name, TEMPLATE_CONFIGS["tech-dark"])

    # 1. 添加背景遮罩
    if config["bg_overlay"][3] > 0:
        overlay = Image.new("RGBA", image.size, config["bg_overlay"])
        image = Image.alpha_composite(image.convert("RGBA"), overlay)

    # 2. 添加标题
    image = add_title_layout(image, title, subtitle, config["title_position"])

    # 3. 添加标签
    if tags:
        image = add_tags(image, tags)

    return image
```

## 失败时的兜底策略

| 失败原因 | 兜底方案 |
|----------|----------|
| 字体缺失 | 使用系统默认中文字体 |
| 文字与背景对比度不足 | 自动添加文字描边或加深遮罩 |
| 标题过长导致换行 | 缩小字号或建议用户精简标题 |
| 模板与图片风格冲突 | 切换到通用模板或纯色背景 |

## 推荐后端实现

### 方式一：Python + Pillow（推荐）

与 `image-compose-local` 共用 Pillow 后端。

### 方式二：Node.js + Sharp + Canvas

```javascript
const { createCanvas, loadImage } = require('canvas');
const sharp = require('sharp');

async function createCoverLayout(sourcePath, title, outputPath) {
  const image = await loadImage(sourcePath);
  const canvas = createCanvas(image.width, image.height);
  const ctx = canvas.getContext('2d');

  // 绘制背景
  ctx.drawImage(image, 0, 0);

  // 添加渐变遮罩
  const gradient = ctx.createLinearGradient(0, image.height * 0.6, 0, image.height);
  gradient.addColorStop(0, 'rgba(0,0,0,0)');
  gradient.addColorStop(1, 'rgba(0,0,0,0.8)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, image.width, image.height);

  // 添加标题
  ctx.font = 'bold 48px "Noto Sans SC"';
  ctx.fillStyle = 'white';
  ctx.textAlign = 'center';
  ctx.shadowColor = 'black';
  ctx.shadowBlur = 4;
  ctx.fillText(title, image.width / 2, image.height * 0.85);

  // 输出
  const buffer = canvas.toBuffer('image/png');
  await sharp(buffer).toFile(outputPath);
}
```

### 方式三：MCP Server 接入

```json
{
  "mcpServers": {
    "design-tools": {
      "command": "npx",
      "args": ["-y", "@modelcontextprovider/design-tools"]
    }
  }
}
```

## 小红书封面尺寸规范

| 类型 | 比例 | 推荐尺寸 | 说明 |
|------|------|----------|------|
| 标准封面 | 3:4 | 1080x1440 | 最常用 |
| 宽封面 | 1:1 | 1080x1080 | 适合横图 |
| 竖封面 | 9:16 | 1080x1920 | 适合全屏 |

**文字安全区**：
- 顶部 15% 避免放置关键文字（可能被 UI 遮挡）
- 底部 20% 留白用于标题
- 左右各 8% 边距

## 与 post-builder 的交接

- 接收 `requirements.md` 中的封面需求
- 读取 `原始素材/` 中的背景图
- 应用模板生成封面
- 输出至 `定稿图/01_cover.png`
- 在 `build-log.md` 中记录：
  - 使用的模板
  - 标题、标签内容
  - 调整细节

## 文件命名规范

```
01_cover.png    # 统一命名
```
