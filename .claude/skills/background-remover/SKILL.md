# Background Remover - 图像去背景技能

## 技能描述

此技能负责图像的背景移除、抠图、透明底 PNG 生成、主体分离等工作，用于制作干净的素材供二次合成使用。

## 用途

- 移除照片背景，生成透明底 PNG
- 提取人物、产品、物体主体
- 制作贴纸、图标素材
- 为合成图准备独立元素
- 去除干扰背景，突出主体

## 适用场景

| 场景 | 说明 |
|------|------|
| 人物抠图 | 从照片中提取人物，用于合成 |
| 产品图 | 电商产品白底图/透明底图 |
| 图标提取 | 从截图中提取图标、按钮 |
| 文字分离 | 从背景中分离文字区域 |
| 主体突出 | 模糊或移除干扰背景 |

## 输入参数

```markdown
- **source**: 源图片路径
- **mode**: 抠图模式
  - `auto`: 自动识别主体（默认）
  - `person`: 人物优先
  - `product`: 产品/物体优先
  - `text`: 文字区域
  - `custom`: 自定义遮罩/选区
- **output_format**: 输出格式
  - `png`: 透明底 PNG（默认）
  - `webp`: 透明底 WebP（更小体积）
- **refine_edges**: 边缘优化（可选）
  - `feather`: 羽化半径（像素）
  - `smooth`: 平滑度
  - `contrast`: 边缘对比度
- **output_name**: 输出文件名
```

## 输出

```
topics/{topic-name}/fig/原始素材/
├── {original_name}_no_bg.png    # 去背景版本
```

或

```
topics/{topic-name}/fig/定稿图/
├── {element_name}.png    # 用于合成的独立元素
```

## 执行步骤

### 方式一：AI 自动抠图（推荐）

使用预训练模型自动识别并移除背景：

```python
# 使用 rembg 库
from rembg import remove
from PIL import Image

def remove_background(input_path, output_path):
    input_image = Image.open(input_path)
    output_image = remove(input_image)
    output_image.save(output_path, format="PNG")
    return output_path
```

### 方式二：人物专用抠图

```python
# 使用人像分割专用模型
from skimage import segmentation
import numpy as np

def extract_person(image_path, output_path):
    # 加载人像分割模型（如 DeepLabV3）
    model = load_person_segmentation_model()

    img = np.array(Image.open(image_path))
    mask = model.predict(img)

    # 提取人物区域
    person_mask = (mask == 12)  # COCO 数据集中 person 类别 ID

    # 应用遮罩
    result = Image.new("RGBA", img.shape[:2][::-1], (0, 0, 0, 0))
    result.paste(Image.fromarray(img), mask=person_mask.astype(np.uint8) * 255)

    result.save(output_path)
    return output_path
```

### 方式三：在线 API（兜底方案）

```python
# 使用 remove.bg API
import requests

def remove_background_api(image_path, output_path, api_key):
    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(image_path, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": api_key},
    )

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    else:
        raise Exception(f"API error: {response.status_code}")
```

## 边缘优化

抠图后通常需要优化边缘，使其更自然：

```python
def refine_edge(image, feather=2, smooth=1, contrast=1.2):
    """
    优化抠图边缘
    - feather: 边缘羽化
    - smooth: 边缘平滑
    - contrast: 边缘对比度
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # 提取 alpha 通道
    alpha = image.split()[3]

    # 应用高斯模糊（羽化）
    if feather > 0:
        alpha = alpha.filter(ImageFilter.GaussianBlur(radius=feather))

    # 调整对比度
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(alpha)
    alpha = enhancer.enhance(contrast)

    # 合并回原图
    image.putalpha(alpha)
    return image
```

## 失败时的兜底策略

| 失败原因 | 兜底方案 |
|----------|----------|
| AI 模型识别错误 | 切换到手动遮罩模式或在线 API |
| 边缘粗糙 | 增加羽化值，或告知用户需要手动精修 |
| 半透明物体（头发、玻璃） | 使用专用模型或 API，或保留部分背景 |
| 复杂背景难以分离 | 建议更换素材或使用模糊背景代替移除 |

## 推荐后端实现

### 方式一：rembg（推荐，免费离线）

```bash
pip install rembg[gpu]  # GPU 加速版本
# 或
pip install rembg  # CPU 版本
```

```python
from rembg import remove

# CLI 使用
# rembg input.png output.png

# Python API
input_image = Image.open("input.png")
output_image = remove(input_image)
output_image.save("output.png")
```

### 方式二：segment-anything (SAM)

```python
# Meta 的 Segment Anything Model
# 更强大但需要更多计算资源
pip install segment-anything

from segment_anything import SamPredictor, sam_model_registry

sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h.pth")
predictor = SamPredictor(sam)

predictor.set_image(np.array(Image.open("input.png")))
masks, scores, logits = predictor.predict()
```

### 方式三：在线 API

| 服务 | 价格 | 说明 |
|------|------|------|
| remove.bg | 免费 50 张/月 | 质量高，需要 API Key |
| clippingmagic.com | 付费 | 批量处理 |
| photoshop API | 付费 | Adobe 生态 |

### 方式四：MCP Server 接入

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

## 输出质量检查

```python
def check_output_quality(image_path):
    """
    检查抠图质量
    """
    img = Image.open(image_path)

    # 检查是否有透明通道
    if img.mode != "RGBA":
        return {"status": "fail", "reason": "No alpha channel"}

    # 检查透明区域占比
    alpha = img.split()[3]
    transparent_pixels = sum(1 for p in alpha.getdata() if p < 128)
    transparent_ratio = transparent_pixels / alpha.width / alpha.height

    # 检查边缘噪点
    # ...

    return {
        "status": "pass" if transparent_ratio > 0.1 else "review",
        "transparent_ratio": transparent_ratio
    }
```

## 与 post-builder 的交接

- 接收需要抠图的素材
- 执行去背景后存入 `原始素材/` 或 `定稿图/`
- 在 `build-log.md` 中记录：
  - 使用的工具/模型
  - 边缘优化参数
  - 质量问题（如有）
- 交由 `image-compose-local` 进行合成（如需要）

## 文件命名规范

```
{original_name}_no_bg.png
{subject}_cutout.png
{element}_transparent.png

示例：
product_shot_no_bg.png
person_cutout.png
icon_transparent.png
```
