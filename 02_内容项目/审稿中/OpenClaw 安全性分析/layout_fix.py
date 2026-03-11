"""
OpenClaw 安全性分析图像排版优化脚本 v3
优化方向：重新排版文字填充留白，保持 9:16 比例，不裁剪
"""

from PIL import Image, ImageDraw, ImageFont
import os

INPUT_DIR = r"C:\Users\pnn\Desktop\socialmedia-work-studio\02_内容项目\审稿中\OpenClaw 安全性分析\fig\optimized"
OUTPUT_DIR = r"C:\Users\pnn\Desktop\socialmedia-work-studio\02_内容项目\审稿中\OpenClaw 安全性分析\fig\optimized"

def get_font(size):
    """获取中文字体"""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",    # 黑体
        "C:/Windows/Fonts/simsun.ttc",    # 宋体
    ]
    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue
    return ImageFont.load_default()

def add_text_to_image(img_path, output_path, additions):
    """在图片上添加文字"""
    img = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    for text_config in additions:
        text = text_config["text"]
        position = text_config["position"]  # (x, y)
        font_size = text_config.get("font_size", 24)
        color = text_config.get("color", (255, 255, 255))
        anchor = text_config.get("anchor", "mm")  # 居中对齐
        shadow = text_config.get("shadow", True)
        
        font = get_font(font_size)
        
        # 计算文字边界框
        bbox = draw.textbbox((0, 0), text, font=font, anchor=anchor)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        # 计算实际绘制位置
        if anchor == "mm":
            x, y = position
            x = x - text_w // 2
            y = y - text_h // 2
        elif anchor == "ma":
            x, y = position
            x = x - text_w // 2
        else:
            x, y = position
        
        # 绘制阴影
        if shadow:
            shadow_offset = 2
            shadow_color = (0, 0, 0, 180)
            draw.text((x + shadow_offset, y + shadow_offset), text, fill=shadow_color, font=font)
        
        # 绘制文字
        draw.text((x, y), text, fill=color, font=font)
    
    img.save(output_path, "PNG", optimize=True)
    print(f"[OK] {os.path.basename(output_path)}")

def main():
    print("=" * 60)
    print("OpenClaw 安全性分析 - 排版优化 v3")
    print("=" * 60)
    print()
    
    # 01_cover: 添加引言
    add_text_to_image(
        os.path.join(INPUT_DIR, "01_cover.png"),
        os.path.join(OUTPUT_DIR, "01_cover.png"),
        [
            {
                "text": "27 万星标的开源项目，背后藏着怎样的安全隐患？",
                "position": (540, 700),
                "font_size": 28,
                "color": (200, 200, 200),
            },
            {
                "text": "从 RCE 漏洞到 ClawJacked 攻击，深度解析 AI 代理的安全边界。",
                "position": (540, 750),
                "font_size": 24,
                "color": (180, 180, 180),
            },
            {
                "text": "↓ 下滑查看完整分析 ↓",
                "position": (540, 1700),
                "font_size": 22,
                "color": (255, 51, 51),
            },
        ]
    )
    
    # 02_architecture: 添加补充说明
    add_text_to_image(
        os.path.join(INPUT_DIR, "02_architecture.png"),
        os.path.join(OUTPUT_DIR, "02_architecture.png"),
        [
            {
                "text": "Gateway 作为中枢，直接调用系统 API。沙箱关闭状态下，",
                "position": (540, 1100),
                "font_size": 24,
                "color": (200, 200, 200),
            },
            {
                "text": "所有命令均在宿主机执行，无隔离保护。",
                "position": (540, 1140),
                "font_size": 24,
                "color": (200, 200, 200),
            },
        ]
    )
    
    # 03_timeline: 添加事件详情（文字在卡片内部）
    add_text_to_image(
        os.path.join(INPUT_DIR, "03_timeline.png"),
        os.path.join(OUTPUT_DIR, "03_timeline.png"),
        [
            {
                "text": "攻击者可远程执行任意代码",
                "position": (540, 220),
                "font_size": 18,
                "color": (200, 200, 200),
            },
            {
                "text": "1.5 万实例存在 RCE 漏洞",
                "position": (540, 360),
                "font_size": 18,
                "color": (200, 200, 200),
            },
            {
                "text": "1184 个恶意技能含窃密脚本",
                "position": (540, 500),
                "font_size": 18,
                "color": (200, 200, 200),
            },
            {
                "text": "CVSS 8.8 高危，任意网站可接管",
                "position": (540, 640),
                "font_size": 18,
                "color": (255, 100, 100),
            },
            {
                "text": "⚠️ 3 个月内 4 起重大安全事件",
                "position": (540, 800),
                "font_size": 24,
                "color": (255, 51, 51),
            },
        ]
    )
    
    # 04_attack_flow: 添加防护建议
    add_text_to_image(
        os.path.join(INPUT_DIR, "04_attack_flow.png"),
        os.path.join(OUTPUT_DIR, "04_attack_flow.png"),
        [
            {
                "text": "防护建议：禁用 WebSocket 连接本地代理 / 设置强密码 / 仅监听 127.0.0.1",
                "position": (540, 1500),
                "font_size": 24,
                "color": (100, 200, 100),
            },
        ]
    )
    
    # 05_risk_matrix: 添加结论
    add_text_to_image(
        os.path.join(INPUT_DIR, "05_risk_matrix.png"),
        os.path.join(OUTPUT_DIR, "05_risk_matrix.png"),
        [
            {
                "text": "企业用户面临全方位高风险，需专业部署方案",
                "position": (540, 1650),
                "font_size": 26,
                "color": (255, 51, 51),
            },
        ]
    )
    
    # 06_checklist: 添加分类和优先级
    add_text_to_image(
        os.path.join(INPUT_DIR, "06_checklist.png"),
        os.path.join(OUTPUT_DIR, "06_checklist.png"),
        [
            {
                "text": "【安装部署】",
                "position": (270, 120),
                "font_size": 20,
                "color": (150, 150, 150),
            },
            {
                "text": "【权限管理】",
                "position": (810, 120),
                "font_size": 20,
                "color": (150, 150, 150),
            },
            {
                "text": "【日常使用】",
                "position": (270, 520),
                "font_size": 20,
                "color": (150, 150, 150),
            },
            {
                "text": "🔴必做：1-4 项   🟡建议：5-10 项",
                "position": (540, 1700),
                "font_size": 22,
                "color": (200, 200, 200),
            },
        ]
    )
    
    # 07_summary: 添加行动呼吁
    add_text_to_image(
        os.path.join(INPUT_DIR, "07_summary.png"),
        os.path.join(OUTPUT_DIR, "07_summary.png"),
        [
            {
                "text": "立即检查你的部署配置 →",
                "position": (540, 1750),
                "font_size": 24,
                "color": (100, 200, 100),
            },
        ]
    )
    
    print()
    print("=" * 60)
    print("排版优化完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
