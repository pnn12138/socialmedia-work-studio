"""
OpenClaw 安全性分析图像修复脚本
修复问题：
1. 背景色从深蓝改为深黑 #050505（暗黑科技风）
2. 07_summary.png 底部添加金句
"""

from PIL import Image, ImageDraw, ImageFont
import os

INPUT_DIR = r"C:\Users\pnn\Desktop\socialmedia-work-studio\02_内容项目\审稿中\OpenClaw 安全性分析\fig\optimized"
OUTPUT_DIR = r"C:\Users\pnn\Desktop\socialmedia-work-studio\02_内容项目\审稿中\OpenClaw 安全性分析\fig\optimized"

# 颜色定义
DARK_BG = (5, 5, 5)  # #050505 深黑
WHITE = (255, 255, 255)
RED_ACCENT = (255, 51, 51)  # #FF3333 高饱和红
BLUE_ACCENT = (59, 130, 246)  # #3B82F6 科技蓝

def adjust_background_color(img_path, output_path, target_bg=DARK_BG):
    """调整图像背景色调为深黑色"""
    img = Image.open(img_path)
    img = img.convert("RGBA")
    
    width, height = img.size
    pixels = img.load()
    
    # 遍历每个像素，将深蓝色区域改为深黑色
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # 检测深蓝色背景区域（蓝色通道明显高于红绿通道）
            if b > r + 30 and b > g + 30 and b < 100:
                # 计算蓝色强度，映射到深黑背景
                blue_intensity = (b - 50) / 50  # 0-1 范围
                # 混合深黑和原色，保留一些渐变
                new_r = int(DARK_BG[0] + (r - DARK_BG[0]) * 0.7)
                new_g = int(DARK_BG[1] + (g - DARK_BG[1]) * 0.7)
                new_b = int(DARK_BG[2] + (b - DARK_BG[2]) * 0.5)
                
                # 确保不超过范围
                new_r = max(5, min(30, new_r))
                new_g = max(5, min(30, new_g))
                new_b = max(5, min(25, new_b))
                
                pixels[x, y] = (new_r, new_g, new_b, a)
    
    img.save(output_path, "PNG", optimize=True)
    print(f"[OK] 背景色调整完成：{os.path.basename(output_path)}")

def add_golden_quote(img_path, output_path, quote_text):
    """在图片底部添加金句"""
    img = Image.open(img_path)
    img = img.convert("RGBA")
    
    width, height = img.size
    
    # 创建绘图对象
    draw = ImageDraw.Draw(img)
    
    # 尝试加载中文字体
    font_paths = [
        "C:/Windows/Fonts/simsun.ttc",      # 宋体
        "C:/Windows/Fonts/simhei.ttf",       # 黑体
        "C:/Windows/Fonts/msyh.ttc",         # 微软雅黑
    ]
    
    font_size = int(width * 0.05)  # 字体大小为宽度的 5%
    
    font = None
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, font_size)
            break
        except:
            continue
    
    if font is None:
        font = ImageFont.load_default()
        print("⚠ 使用中文字体失败，使用默认字体")
    
    # 金句文本
    quote_line1 = "功能即风险边界"
    quote_line2 = "越像操作系统的工具，越需要专业部署"
    
    # 计算文字位置（底部居中）
    bbox1 = draw.textbbox((0, 0), quote_line1, font=font)
    bbox2 = draw.textbbox((0, 0), quote_line2, font=font)
    
    text_width1 = bbox1[2] - bbox1[0]
    text_width2 = bbox2[2] - bbox2[0]
    text_height = bbox1[3] - bbox1[1]
    
    # 起始 y 坐标（底部向上 8%）
    start_y = int(height * 0.82)
    
    # 绘制文字（带阴影效果）
    shadow_offset = 2
    shadow_color = (0, 0, 0, 180)
    text_color = RED_ACCENT  # 使用高饱和红
    
    # 第一行（带阴影）
    x1 = (width - text_width1) // 2
    draw.text((x1 + shadow_offset, start_y + shadow_offset), quote_line1, fill=shadow_color, font=font)
    draw.text((x1, start_y), quote_line1, fill=text_color, font=font)
    
    # 第二行（带阴影）
    x2 = (width - text_width2) // 2
    draw.text((x2 + shadow_offset, start_y + text_height + 5 + shadow_offset), quote_line2, fill=shadow_color, font=font)
    draw.text((x2, start_y + text_height + 5), quote_line2, fill=text_color, font=font)
    
    img.save(output_path, "PNG", optimize=True)
    print(f"[OK] 金句添加完成：{os.path.basename(output_path)}")

def main():
    print("=" * 60)
    print("OpenClaw 安全性分析 - 图像修复")
    print("=" * 60)
    print()
    
    # 1. 调整所有图片的背景色
    print("【步骤 1】调整背景色为深黑 #050505")
    print("-" * 40)
    
    files = [
        "01_cover.png",
        "02_architecture.png",
        "03_timeline.png",
        "04_attack_flow.png",
        "05_risk_matrix.png",
        "06_checklist.png",
        "07_summary.png",
    ]
    
    for filename in files:
        input_path = os.path.join(INPUT_DIR, filename)
        if os.path.exists(input_path):
            adjust_background_color(input_path, input_path)
        else:
            print(f"[ERR] 文件不存在：{filename}")
    
    print()
    
    # 2. 为 07_summary.png 添加金句
    print("【步骤 2】为 07_summary.png 添加金句")
    print("-" * 40)
    
    summary_path = os.path.join(INPUT_DIR, "07_summary.png")
    if os.path.exists(summary_path):
        add_golden_quote(
            summary_path,
            summary_path,
            "功能即风险边界，越像操作系统的工具越需要专业部署"
        )
    else:
        print("[ERR] 07_summary.png 不存在")
    
    print()
    print("=" * 60)
    print("修复完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
