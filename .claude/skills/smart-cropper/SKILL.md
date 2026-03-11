# Smart Cropper - 智能裁剪技能

## 技能描述

基于主体检测（人脸、物体）自动确定最佳裁剪区域的智能裁剪工具。
支持多种裁剪模式和焦点检测，让裁剪更智能、更精准。

## 快速开始

```bash
# 智能裁剪（自动检测人脸）
/smart-cropper input.jpg -o output.jpg --ratio 3:4

# 分析图片（检测人脸、显著区域）
/smart-cropper input.jpg --analyze

# 指定焦点模式
/smart-cropper input.jpg -o output.jpg --ratio 16:9 --focus face
```

## 使用方式

### 基础用法

```bash
# 裁剪为小红书封面比例（3:4）
/smart-cropper input.jpg -o output.jpg --ratio 3:4

# 裁剪为今日头条封面（16:9）
/smart-cropper input.jpg -o output.jpg --ratio 16:9

# 裁剪为正方形（1:1）
/smart-cropper input.jpg -o output.jpg --ratio 1:1
```

### 焦点模式

```bash
# 自动检测（优先人脸，其次显著区域）
/smart-cropper input.jpg -o output.jpg --ratio 3:4 --focus auto

# 强制人脸优先
/smart-cropper input.jpg -o output.jpg --ratio 3:4 --focus face

# 眼睛优先（适合人像特写）
/smart-cropper input.jpg -o output.jpg --ratio 3:4 --focus eye

# 显著区域优先
/smart-cropper input.jpg -o output.jpg --ratio 3:4 --focus salient

# 固定焦点
/smart-cropper input.jpg -o output.jpg --ratio 3:4 --focus center
/smart-cropper input.jpg -o output.jpg --ratio 3:4 --focus top
/smart-cropper input.jpg -o output.jpg --ratio 3:4 --focus bottom
```

### 分析图片

```bash
# 分析图片内容（检测人脸、显著区域等）
/smart-cropper input.jpg --analyze
```

输出示例：
```json
{
  "width": 1920,
  "height": 1080,
  "faces": 2,
  "face_regions": [
    {"x": 500, "y": 300, "w": 200, "h": 200},
    {"x": 1200, "y": 350, "w": 180, "h": 180}
  ],
  "eyes": 4,
  "salient_region": {"x": 480, "y": 270, "w": 960, "h": 540},
  "recommended_focus": "face"
}
```

## 输入参数

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `input` | 输入图片路径 | 必需 |
| `-o, --output` | 输出图片路径 | 必需 |
| `--ratio` | 目标比例 | "3:4", "16:9", "1:1" 等 |
| `--focus` | 焦点模式 | `auto`（默认）, `face`, `eye`, `center`, `top`, `bottom`, `left`, `right`, `salient` |
| `--min-face-size` | 最小人脸尺寸 | 默认 50（像素） |
| `--analyze` | 仅分析不裁剪 | 标志 |

## 输出

```
topics/{topic-name}/fig/原始素材/
├── 01_cover_cropped.png    # 裁剪后的封面素材
├── 02_inner_cropped.png    # 裁剪后的内页素材
└── ...
```

## 焦点模式说明

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `auto` | 自动检测，优先人脸，其次显著区域 | 通用场景，推荐 |
| `face` | 强制检测人脸，以人脸为中心 | 人像照片 |
| `eye` | 检测眼睛，确定视觉焦点 | 人像特写 |
| `salient` | 检测显著区域（梯度最大处） | 产品图、物体 |
| `center` | 以图片中心为裁剪中心 | 对称构图 |
| `top` | 聚焦上方 | 天空、建筑 |
| `bottom` | 聚焦下方 | 地面、水面 |
| `left` | 聚焦左侧 | 左向构图 |
| `right` | 聚焦右侧 | 右向构图 |

## 环境要求

- Python 3.8+
- OpenCV (`pip install opencv-python`)
- Pillow (`pip install pillow`)
- NumPy (`pip install numpy`)

## 安装依赖

```bash
pip install opencv-python pillow numpy
```

## 技术原理

### 人脸检测
使用 OpenCV 内置的 Haar Cascade 分类器：
- `haarcascade_frontalface_default.xml` - 正面人脸
- `haarcascade_profileface.xml` - 侧面人脸

### 显著区域检测
1. 转换为 Lab 颜色空间
2. 计算 L 通道的梯度幅值
3. Otsu 二值化
4. 形态学操作
5. 查找最大轮廓作为显著区域

### 裁剪算法
1. 确定焦点位置（人脸中心/显著区域中心/指定位置）
2. 根据目标比例计算裁剪区域
3. 确保裁剪区域在图像范围内
4. 围绕焦点执行裁剪

## 与 post-builder 的交接

- 接收来自 `原始素材/` 的图片
- 按 `requirements.md` 中的裁剪需求执行
- 输出至 `原始素材/` 或 `定稿图/`
- 在 `build-log.md` 中记录：
  - 使用的焦点模式
  - 检测到的主体（人脸数量、位置）
  - 裁剪前后的尺寸

## 失败时的兜底策略

| 失败原因 | 兜底方案 |
|----------|----------|
| 未检测到人脸 | 回退到显著区域检测 |
| 显著区域检测失败 | 回退到中心裁剪 |
| OpenCV 不可用 | 降级到普通裁剪（按焦点位置） |
| 图片过小 | 告知用户，建议更换素材 |

## 使用示例

### 示例 1：人像照片裁剪

```bash
# 原始图片：1920x1080，含人脸
# 目标：小红书封面 3:4

/smart-cropper portrait.jpg -o portrait_cropped.jpg --ratio 3:4 --focus auto
```

### 示例 2：产品图裁剪

```bash
# 原始图片：产品位于画面中央
# 目标：正方形产品图

/smart-cropper product.jpg -o product_cropped.jpg --ratio 1:1 --focus salient
```

### 示例 3：风景图裁剪

```bash
# 原始图片：16:9 风景
# 目标：9:16 竖版

/smart-cropper landscape.jpg -o landscape_cropped.jpg --ratio 9:16 --focus top
```

## 批量处理

```bash
# 批量裁剪（shell 脚本）
for img in *.jpg; do
    smart_cropper.py "$img" -o "cropped_$img" --ratio 3:4
done
```
