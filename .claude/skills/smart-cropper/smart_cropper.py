#!/usr/bin/env python3
"""
Smart Cropper - 智能裁剪脚本

基于主体检测（人脸、物体）自动确定最佳裁剪区域
支持多种裁剪模式和焦点检测

依赖：
- pip install opencv-python
- pip install pillow
- pip install numpy
- pip install python-dotenv
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 加载根目录 .env 文件
try:
    from dotenv import load_dotenv
    # 查找根目录.env 文件
    def find_root_env():
        """向上查找根目录的.env 文件"""
        current = Path(__file__).resolve()
        # 向上查找 5 层
        for _ in range(5):
            current = current.parent
            env_path = current / '.env'
            if env_path.exists():
                return env_path
        return None

    root_env = find_root_env()
    if root_env:
        load_dotenv(dotenv_path=root_env)
except ImportError:
    pass  # python-dotenv 未安装则跳过

try:
    import cv2
    import numpy as np
    from PIL import Image
except ImportError as e:
    print(f"Error: Missing dependency. Please run: pip install {str(e).split()[-1]}")
    sys.exit(1)


# 预训练模型路径（OpenCV 内置）
CASCADE_PATHS = {
    "face": cv2.data.haarcascades + "haarcascade_frontalface_default.xml",
    "face_profile": cv2.data.haarcascades + "haarcascade_profileface.xml",
    "eye": cv2.data.haarcascades + "haarcascade_eye.xml",
    "eye_russian": cv2.data.haarcascades + "haarcascade_russian_eye.xml",
    "smile": cv2.data.haarcascades + "haarcascade_smile.xml",
    "upperbody": cv2.data.haarcascades + "haarcascade_upperbody.xml",
    "fullbody": cv2.data.haarcascades + "haarcascade_fullbody.xml",
}


def load_cascade(cascade_type):
    """
    加载 Cascade 分类器

    Args:
        cascade_type: 分类器类型 "face", "eye", "smile", "upperbody", "fullbody"

    Returns:
        cv2.CascadeClassifier 对象
    """
    path = CASCADE_PATHS.get(cascade_type)
    if not path or not Path(path).exists():
        return None
    return cv2.CascadeClassifier(path)


def detect_faces(image_cv):
    """
    检测人脸

    Args:
        image_cv: OpenCV 图像（BGR）

    Returns:
        人脸矩形框列表 [(x, y, w, h), ...]
    """
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # 尝试正面人脸检测
    face_cascade = load_cascade("face")
    if face_cascade:
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        if len(faces) > 0:
            return [(x, y, w, h) for (x, y, w, h) in faces]

    # 尝试侧面人脸检测
    profile_cascade = load_cascade("face_profile")
    if profile_cascade:
        faces = profile_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        if len(faces) > 0:
            return [(x, y, w, h) for (x, y, w, h) in faces]

    return []


def detect_eyes(image_cv):
    """
    检测眼睛（用于确定人脸焦点）

    Args:
        image_cv: OpenCV 图像（BGR）

    Returns:
        眼睛矩形框列表
    """
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    eye_cascade = load_cascade("eye")

    if eye_cascade:
        eyes = eye_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20)
        )
        return [(x, y, w, h) for (x, y, w, h) in eyes]

    return []


def detect_salient_region(image_cv):
    """
    检测显著区域（使用简单 saliency 检测）

    Args:
        image_cv: OpenCV 图像（BGR）

    Returns:
        (x, y, w, h) 显著区域
    """
    # 转换为 Lab 颜色空间
    lab = cv2.cvtColor(image_cv, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # 计算每个通道的梯度
    grad_x = cv2.Sobel(l, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(l, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)

    # 二值化
    _, binary = cv2.threshold(gradient_magnitude, 0, 255, cv2.THRESH_OTSU)
    binary = np.uint8(binary)

    # 形态学操作
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # 找到最大轮廓
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return (x, y, w, h)

    # 回退到中心区域
    h, w = image_cv.shape[:2]
    return (w // 4, h // 4, w // 2, h // 2)


def smart_crop_pil(image, target_ratio, focus="auto", min_face_size=50):
    """
    智能裁剪（PIL Image 接口）

    Args:
        image: PIL Image 对象
        target_ratio: 目标比例（float，宽/高）
        focus: 焦点模式 "auto", "face", "center", "top", "bottom"
        min_face_size: 最小人脸尺寸（像素）

    Returns:
        裁剪后的 PIL Image 对象
    """
    # 转换为 OpenCV 格式
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # 检测焦点
    if focus == "auto" or focus == "face":
        faces = detect_faces(image_cv)

        if faces:
            # 选择最大的人脸
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            fx, fy, fw, fh = largest_face

            # 计算以人脸为中心的裁剪区域
            center_x = fx + fw // 2
            center_y = fy + fh // 2

            return crop_around_point_pil(image, target_ratio, (center_x, center_y))

    elif focus == "eye":
        eyes = detect_eyes(image_cv)
        if eyes:
            # 计算眼睛区域的中心
            eye_centers = [(e[0] + e[2] // 2, e[1] + e[3] // 2) for e in eyes]
            avg_x = sum(c[0] for c in eye_centers) // len(eye_centers)
            avg_y = sum(c[1] for c in eye_centers) // len(eye_centers)
            return crop_around_point_pil(image, target_ratio, (avg_x, avg_y))

    # 回退到其他模式
    if focus == "auto":
        # 尝试显著区域检测
        region = detect_salient_region(image_cv)
        rx, ry, rw, rh = region
        center_x = rx + rw // 2
        center_y = ry + rh // 2
        return crop_around_point_pil(image, target_ratio, (center_x, center_y))

    # 固定焦点模式
    return crop_with_focus_pil(image, target_ratio, focus)


def crop_around_point_pil(image, target_ratio, center_point):
    """
    围绕指定点裁剪

    Args:
        image: PIL Image 对象
        target_ratio: 目标比例（宽/高）
        center_point: 中心点 (x, y)

    Returns:
        裁剪后的 PIL Image 对象
    """
    w, h = image.size
    cx, cy = center_point

    # 计算裁剪区域
    if target_ratio > 1:
        # 横向
        new_w = min(w, int(h * target_ratio))
        new_h = int(new_w / target_ratio)
    else:
        # 纵向
        new_h = min(h, int(w / target_ratio))
        new_w = int(new_h * target_ratio)

    # 确保在图像范围内
    left = max(0, min(cx - new_w // 2, w - new_w))
    top = max(0, min(cy - new_h // 2, h - new_h))
    right = left + new_w
    bottom = top + new_h

    return image.crop((left, top, right, bottom))


def crop_with_focus_pil(image, target_ratio, focus):
    """
    按固定焦点裁剪

    Args:
        image: PIL Image 对象
        target_ratio: 目标比例
        focus: "center", "top", "bottom", "left", "right"

    Returns:
        裁剪后的 PIL Image 对象
    """
    w, h = image.size

    # 计算新尺寸
    if target_ratio > 1:
        new_w = min(w, int(h * target_ratio))
        new_h = int(new_w / target_ratio)
    else:
        new_h = min(h, int(w / target_ratio))
        new_w = int(new_h * target_ratio)

    # 计算起始位置
    if focus == "center":
        x = (w - new_w) // 2
        y = (h - new_h) // 2
    elif focus == "top":
        x = (w - new_w) // 2
        y = 0
    elif focus == "bottom":
        x = (w - new_w) // 2
        y = h - new_h
    elif focus == "left":
        x = 0
        y = (h - new_h) // 2
    elif focus == "right":
        x = w - new_w
        y = (h - new_h) // 2
    else:
        x = (w - new_w) // 2
        y = (h - new_h) // 2

    return image.crop((x, y, x + new_w, y + new_h))


def analyze_image(image_path):
    """
    分析图片内容（检测人脸、眼睛等）

    Args:
        image_path: 图片路径

    Returns:
        分析结果字典
    """
    image_pil = Image.open(image_path)
    image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    faces = detect_faces(image_cv)
    eyes = detect_eyes(image_cv) if faces else []
    salient = detect_salient_region(image_cv)

    return {
        "width": image_pil.width,
        "height": image_pil.height,
        "faces": len(faces),
        "face_regions": [{"x": f[0], "y": f[1], "w": f[2], "h": f[3]} for f in faces],
        "eyes": len(eyes),
        "salient_region": {"x": salient[0], "y": salient[1], "w": salient[2], "h": salient[3]},
        "recommended_focus": "face" if faces else "auto",
    }


def main():
    parser = argparse.ArgumentParser(description="Smart Cropper - 智能裁剪工具")
    parser.add_argument("input", help="输入图片路径")
    parser.add_argument("-o", "--output", required=True, help="输出图片路径")
    parser.add_argument("--ratio", required=True, help="目标比例，如 3:4, 16:9, 1:1")
    parser.add_argument("--focus", default="auto",
                        choices=["auto", "face", "eye", "center", "top", "bottom", "left", "right", "salient"],
                        help="焦点模式")
    parser.add_argument("--analyze", action="store_true", help="仅分析图片，不执行裁剪")
    parser.add_argument("--min-face-size", type=int, default=50, help="最小人脸尺寸（像素）")

    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    image = Image.open(args.input)

    # 分析模式
    if args.analyze:
        result = analyze_image(args.input)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # 解析比例
    try:
        if ":" in args.ratio:
            parts = args.ratio.split(":")
            target_ratio = float(parts[0]) / float(parts[1])
        else:
            target_ratio = float(args.ratio)
    except ValueError:
        print(f"Error: Invalid ratio format: {args.ratio}")
        sys.exit(1)

    # 执行智能裁剪
    cropped = smart_crop_pil(
        image,
        target_ratio,
        focus=args.focus,
        min_face_size=args.min_face_size
    )

    # 保存结果
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    cropped.save(args.output, quality=95)
    print(f"Smart cropped saved to: {args.output}")
    print(f"Original size: {image.width}x{image.height}")
    print(f"Cropped size: {cropped.width}x{cropped.height}")


if __name__ == "__main__":
    main()
