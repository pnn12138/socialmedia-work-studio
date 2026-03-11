#!/usr/bin/env python3
"""
Image Compose Local - 本地图像合成与编辑脚本

支持功能：
- 裁剪图片至目标比例
- 调整图片分辨率与尺寸
- 多图拼接（横向、纵向、网格）
- 添加文字标题、标签、说明
- 图层叠加与混合
- 制作信息卡片、对比图
- 调整色调、亮度、对比度
- 添加边框、装饰元素

依赖：pip install pillow python-dotenv
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 加载根目录 .env 文件
try:
    from dotenv import load_dotenv
    # 查找根目录 .env 文件
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
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
except ImportError:
    print("Error: Pillow not installed. Please run: pip install pillow")
    sys.exit(1)

