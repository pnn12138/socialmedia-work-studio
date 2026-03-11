# Image Export QC - 图像导出与质量检查技能

## 技能描述

此技能负责图像的最终导出、尺寸检查、比例验证、分辨率确认、文件命名规范检查与来源记录，是定稿图发布前的最后一道质量关卡。

## 用途

- 导出图像至目标格式（PNG, JPG, WebP）
- 检查图像尺寸是否符合平台要求
- 验证图像比例是否正确
- 检查分辨率是否满足发布标准
- 执行文件命名规范检查
- 记录图片来源与授权信息
- 生成图像使用清单

## 适用场景

| 场景 | 说明 |
|------|------|
| 发布前检查 | 确保所有图像符合平台规范 |
| 批量导出 | 统一导出多张定稿图 |
| 来源审计 | 检查图片版权与授权记录 |
| 质量把关 | 拦截低分辨率、比例错误的图像 |
| 归档管理 | 建立图像使用档案 |

## 输入参数

```markdown
- **source_dir**: 源图像目录（如 `定稿图/`）
- **output_format**: 输出格式
  - `png`: 无损质量（默认）
  - `jpg`: 有损压缩，更小体积
  - `webp`: 现代格式，最佳压缩率
- **quality**: 压缩质量（JPG/WebP）
  - 范围：1-100，默认 90
- **target_platform**: 目标平台
  - `xiaohongshu`: 小红书规范
  - `toutiao`: 今日头条规范
  - `wechat`: 微信公众号规范
- **check_list**: 检查项目
  - `dimensions`: 尺寸检查
  - `ratio`: 比例检查
  - `resolution`: 分辨率检查
  - `naming`: 命名规范检查
  - `attribution`: 来源授权检查
- **output_dir**: 输出目录（可选，默认覆盖原文件）
```

## 输出

```
topics/{topic-name}/fig/定稿图/
├── 01_cover.png              # 导出文件
├── 02_inner_01.png
├── ...
└── export_qc_report.md       # 质量检查报告

topics/{topic-name}/fig/
├── images_attribution.md     # 图片来源清单
```

## 平台尺寸规范

### 小红书

| 类型 | 比例 | 最小尺寸 | 推荐尺寸 | 最大尺寸 |
|------|------|----------|----------|----------|
| 封面/内页 | 3:4 | 720x960 | 1080x1440 | 2160x2880 |
| 正方形 | 1:1 | 720x720 | 1080x1080 | 2160x2160 |
| 横版 | 16:9 | 1280x720 | 1920x1080 | 3840x2160 |
| 竖版 | 9:16 | 720x1280 | 1080x1920 | 2160x3840 |

- 文件格式：JPG, PNG
- 文件大小：单张 ≤ 10MB
- 色彩模式：RGB

### 今日头条

| 类型 | 比例 | 推荐尺寸 |
|------|------|----------|
| 文章封面 | 16:9 | 1280x720 |
| 竖版封面 | 3:4 | 750x1000 |
| 插图 | 灵活 | 宽度 ≥ 800 |

### 微信公众号

| 类型 | 比例 | 推荐尺寸 |
|------|------|----------|
| 封面大图 | 2.35:1 | 900x383 |
| 封面小图 | 1:1 | 200x200 |
| 正文插图 | 灵活 | 宽度 1080 |

## 执行步骤

### 1. 尺寸与比例检查

```python
def check_dimensions(image_path, platform="xiaohongshu"):
    """
    检查图像尺寸和比例
    """
    from PIL import Image

    img = Image.open(image_path)
    w, h = img.size

    # 平台规范
    PLATFORM_SPECS = {
        "xiaohongshu": {
            "ratios": [(3, 4), (1, 1), (16, 9), (9, 16)],
            "min_width": 720,
            "min_height": 720,
            "max_width": 4096,
            "max_height": 4096,
        },
        "toutiao": {
            "ratios": [(16, 9), (3, 4), (1, 1)],
            "min_width": 800,
            "min_height": 600,
        },
        "wechat": {
            "ratios": [(2.35, 1), (1, 1), (3, 2)],
            "min_width": 900,
            "min_height": 383,
        },
    }

    spec = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["xiaohongshu"])

    # 检查实际比例
    actual_ratio = w / h
    ratio_tolerance = 0.05  # 5% 容差

    ratio_match = False
    matched_ratio = None

    for rw, rh in spec["ratios"]:
        target_ratio = rw / rh
        if abs(actual_ratio - target_ratio) < ratio_tolerance:
            ratio_match = True
            matched_ratio = f"{rw}:{rh}"
            break

    # 生成报告
    result = {
        "file": image_path,
        "dimensions": f"{w}x{h}",
        "ratio": f"{actual_ratio:.2f} ({matched_ratio or '未匹配标准比例'})",
        "ratio_pass": ratio_match,
        "size_pass": (
            w >= spec.get("min_width", 720) and
            h >= spec.get("min_height", 720) and
            w <= spec.get("max_width", 4096) and
            h <= spec.get("max_height", 4096)
        ),
    }

    return result
```

### 2. 分辨率检查

```python
def check_resolution(image_path, min_dpi=72):
    """
    检查图像分辨率（DPI）
    """
    from PIL import Image

    img = Image.open(image_path)
    dpi = img.info.get('dpi', (72, 72))

    if isinstance(dpi, (int, float)):
        dpi = (dpi, dpi)

    horizontal_dpi, vertical_dpi = dpi

    return {
        "horizontal_dpi": horizontal_dpi,
        "vertical_dpi": vertical_dpi,
        "pass": horizontal_dpi >= min_dpi and vertical_dpi >= min_dpi,
    }
```

### 3. 文件命名规范检查

```python
import re

def check_naming_convention(file_path):
    """
    检查文件命名是否符合规范
    期望格式：NN_type_description.ext
    - NN: 两位数字序号
    - type: 类型 (cover, inner)
    - description: 可选描述
    """
    filename = os.path.basename(file_path)
    pattern = r'^\d{2}_(cover|inner_\d+)(_[a-zA-Z0-9_-]+)?\.(png|jpg|jpeg|webp)$'

    match = re.match(pattern, filename, re.IGNORECASE)

    return {
        "file": filename,
        "pass": match is not None,
        "expected_format": "NN_type_description.ext",
    }
```

### 4. 来源授权检查

```python
def check_attribution(topic_dir):
    """
    检查图片来源记录是否完整
    """
    # 读取 requirements.md
    req_path = os.path.join(topic_dir, "fig", "requirements.md")
    search_results_path = os.path.join(topic_dir, "fig", "search-results.md")
    original_assets_readme = os.path.join(topic_dir, "fig", "原始素材", "README.md")

    attribution_status = {
        "requirements_exists": os.path.exists(req_path),
        "search_results_exists": os.path.exists(search_results_path),
        "assets_readme_exists": os.path.exists(original_assets_readme),
        "missing_sources": [],
    }

    # 检查是否有未记录来源的图片
    # ...

    return attribution_status
```

### 5. 批量导出

```python
def export_images(source_dir, output_format="png", quality=90, target_size=None):
    """
    批量导出图像
    """
    from PIL import Image
    import os

    exported = []
    errors = []

    for filename in sorted(os.listdir(source_dir)):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            continue

        source_path = os.path.join(source_dir, filename)
        base_name = os.path.splitext(filename)[0]

        try:
            img = Image.open(source_path)

            # 转换模式（如 RGBA → RGB for JPG）
            if output_format.lower() == 'jpg' and img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background

            # 调整尺寸（如需要）
            if target_size:
                img = img.resize(target_size, Image.LANCZOS)

            # 导出
            output_path = os.path.join(source_dir, f"{base_name}.{output_format}")
            save_kwargs = {"quality": quality} if output_format.lower() in ['jpg', 'webp'] else {}
            img.save(output_path, format=output_format.upper(), **save_kwargs)

            exported.append({
                "source": source_path,
                "output": output_path,
                "format": output_format,
            })

        except Exception as e:
            errors.append({
                "file": filename,
                "error": str(e),
            })

    return {"exported": exported, "errors": errors}
```

## 失败时的兜底策略

| 失败原因 | 兜底方案 |
|----------|----------|
| 图片尺寸过小 | 尝试 upscale 或告知用户更换素材 |
| 比例不匹配 | 自动裁剪至最近的标准比例，或报告用户 |
| 格式转换失败 | 保留原格式，记录原因 |
| 来源记录缺失 | 生成待补充清单，标注高风险项 |

## 质量检查报告格式

```markdown
# 图像导出质量检查报告

**主题**: {topic-name}
**检查时间**: {timestamp}
**目标平台**: {platform}

## 总览

| 检查项 | 通过数 | 失败数 | 状态 |
|--------|--------|--------|------|
| 尺寸检查 | 5/5 | 0 | ✅ |
| 比例检查 | 4/5 | 1 | ⚠️ |
| 分辨率检查 | 5/5 | 0 | ✅ |
| 命名规范 | 5/5 | 0 | ✅ |
| 来源授权 | 4/5 | 1 | ⚠️ |

## 详细结果

### 01_cover.png
- 尺寸：1080x1440 ✅
- 比例：0.75 (3:4) ✅
- 分辨率：72 DPI ✅
- 命名：规范 ✅
- 来源：已记录 ✅

### 02_inner_01.png
...

## 待修复问题

1. **03_inner_02.png** - 比例不匹配标准（实际 1.52，期望 1.50）
2. **05_inner_04.png** - 来源记录缺失摄影师姓名

## 建议

- 建议替换 03_inner_02.png 为更接近 3:4 比例的版本
- 补充 05_inner_04.png 的来源信息
```

## 推荐后端实现

### 方式一：Python + Pillow（推荐）

与 `image-compose-local` 共用 Pillow 后端。

### 方式二：Node.js + Sharp

```javascript
const sharp = require('sharp');

async function exportImage(input, output, options = {}) {
  let pipeline = sharp(input);

  if (options.resize) {
    pipeline = pipeline.resize(options.resize.width, options.resize.height);
  }

  if (options.format === 'jpg') {
    pipeline = pipeline.jpeg({ quality: options.quality || 90 });
  } else if (options.format === 'webp') {
    pipeline = pipeline.webp({ quality: options.quality || 90 });
  } else {
    pipeline = pipeline.png();
  }

  await pipeline.toFile(output);
}
```

### 方式三：MCP Server 接入

```json
{
  "mcpServers": {
    "image-tools": {
      "command": "npx",
      "args": ["-y", "@modelcontextprovider/image-tools"]
    }
  }
}
```

## 与 post-builder 的交接

- 在 post-builder 完成所有图像处理后执行
- 检查所有定稿图的质量
- 生成 `export_qc_report.md`
- 生成 `images_attribution.md`
- 如有问题，在 `build-log.md` 中记录并要求返工
- 通过后，图像可进入发布流程

## 文件命名规范

```
定稿图文件：
NN_type_description.ext

示例：
01_cover.png
02_inner_01.png
03_inner_02_architecture.png
04_inner_03_threats.png
05_inner_04_protection.png

报告文件：
export_qc_report.md
images_attribution.md
```
