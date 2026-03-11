"""
OpenClaw 安全性分析图像排版优化脚本 v4
根据主人建议精准优化：
1. 01_cover: 底部引导图标字体放大
2. 02_architecture: 增加内容，数字改单列
3. 03/04/05/07: 增加文字/增大字体
4. 06_checklist: 增大字体
"""

from PIL import Image, ImageDraw, ImageFont
import os

INPUT_DIR = r"C:\Users\pnn\Desktop\socialmedia-work-studio\02_内容项目\审稿中\OpenClaw 安全性分析\fig\output"
OUTPUT_DIR = r"C:\Users\pnn\Desktop\socialmedia-work-studio\02_内容项目\审稿中\OpenClaw 安全性分析\fig\optimized"

def get_font(size):
    """获取中文字体"""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue
    return ImageFont.load_default()

def draw_text_with_shadow(draw, position, text, font, color, shadow=True):
    """绘制带阴影的文字"""
    x, y = position
    if shadow:
        # 黑色阴影
        draw.text((x+2, y+2), text, fill=(0, 0, 0, 180), font=font)
    draw.text((x, y), text, fill=color, font=font)

def process_image(img_path, output_path, draw_func):
    """处理图片"""
    img = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    draw_func(draw, img.size)
    img.save(output_path, "PNG", optimize=True)
    print(f"[OK] {os.path.basename(output_path)}")

def main():
    print("=" * 60)
    print("OpenClaw 安全性分析 - 排版优化 v4")
    print("=" * 60)
    print()
    
    # ========== 01_cover: 放大底部引导 ==========
    process_image(
        os.path.join(INPUT_DIR, "01_cover.png"),
        os.path.join(OUTPUT_DIR, "01_cover.png"),
        lambda draw, size: [
            # 引言 - 白色加大
            draw_text_with_shadow(draw, (540, 680), 
                "27 万星标的开源项目，背后藏着怎样的安全隐患？", 
                get_font(32), (255, 255, 255)),
            draw_text_with_shadow(draw, (540, 730), 
                "从 RCE 漏洞到 ClawJacked 攻击，深度解析 AI 代理的安全边界。", 
                get_font(28), (230, 230, 230)),
            # 底部引导 - 放大
            draw_text_with_shadow(draw, (540, 1600), 
                "⬇️ 下滑查看完整分析 ⬇️", 
                get_font(36), (255, 80, 80)),
        ]
    )
    
    # ========== 02_architecture: 改单列 + 增加内容 ==========
    process_image(
        os.path.join(INPUT_DIR, "02_architecture.png"),
        os.path.join(OUTPUT_DIR, "02_architecture.png"),
        lambda draw, size: [
            # 补充说明 - 白色加大，位置上移
            draw_text_with_shadow(draw, (540, 950), 
                "Gateway 作为中枢，直接调用系统 API", 
                get_font(28), (255, 255, 255)),
            draw_text_with_shadow(draw, (540, 990), 
                "沙箱关闭状态下，所有命令均在宿主机执行", 
                get_font(28), (255, 255, 255)),
            draw_text_with_shadow(draw, (540, 1040), 
                "⚠️ 无隔离保护 = 任意代码可读写你的文件/执行命令", 
                get_font(26), (255, 80, 80)),
        ]
    )
    
    # ========== 03_timeline: 增加详情 + 下移 ==========
    process_image(
        os.path.join(INPUT_DIR, "03_timeline.png"),
        os.path.join(OUTPUT_DIR, "03_timeline.png"),
        lambda draw, size: [
            # 事件详情 - 在卡片右侧
            draw_text_with_shadow(draw, (700, 210), 
                "攻击者可远程执行任意代码", 
                get_font(22), (220, 220, 220)),
            draw_text_with_shadow(draw, (700, 350), 
                "1.5 万实例存在 RCE 漏洞", 
                get_font(22), (220, 220, 220)),
            draw_text_with_shadow(draw, (700, 490), 
                "1184 个恶意技能含窃密脚本", 
                get_font(22), (220, 220, 220)),
            draw_text_with_shadow(draw, (700, 630), 
                "CVSS 8.8 高危，任意网站可接管", 
                get_font(22), (255, 100, 100)),
            # 总结条 - 下移
            draw_text_with_shadow(draw, (540, 850), 
                "⚠️ 3 个月内 4 起重大安全事件", 
                get_font(30), (255, 80, 80)),
        ]
    )
    
    # ========== 04_attack_flow: 放大防护建议 ==========
    process_image(
        os.path.join(INPUT_DIR, "04_attack_flow.png"),
        os.path.join(OUTPUT_DIR, "04_attack_flow.png"),
        lambda draw, size: [
            # 防护建议 - 白色 + 绿色，放大
            draw_text_with_shadow(draw, (540, 1400), 
                "🛡️ 防护建议", 
                get_font(32), (255, 255, 255)),
            draw_text_with_shadow(draw, (540, 1450), 
                "禁用 WebSocket 连接本地代理", 
                get_font(26), (150, 255, 150)),
            draw_text_with_shadow(draw, (540, 1490), 
                "设置强密码 / 仅监听 127.0.0.1", 
                get_font(26), (150, 255, 150)),
        ]
    )
    
    # ========== 05_risk_matrix: 放大结论 ==========
    process_image(
        os.path.join(INPUT_DIR, "05_risk_matrix.png"),
        os.path.join(OUTPUT_DIR, "05_risk_matrix.png"),
        lambda draw, size: [
            # 结论 - 白色 + 红色描边
            draw_text_with_shadow(draw, (540, 1600), 
                "📊 企业用户面临全方位高风险", 
                get_font(30), (255, 255, 255)),
            draw_text_with_shadow(draw, (540, 1650), 
                "需专业部署方案 + 最小权限隔离", 
                get_font(28), (255, 100, 100)),
        ]
    )
    
    # ========== 06_checklist: 增大字体 + 修正分类 ==========
    process_image(
        os.path.join(INPUT_DIR, "06_checklist.png"),
        os.path.join(OUTPUT_DIR, "06_checklist.png"),
        lambda draw, size: [
            # 分类标题 - 修正位置
            draw_text_with_shadow(draw, (270, 80), "【安装部署】", get_font(24), (180, 180, 180)),
            draw_text_with_shadow(draw, (810, 80), "【权限管理】", get_font(24), (180, 180, 180)),
            draw_text_with_shadow(draw, (270, 480), "【日常使用】", get_font(24), (180, 180, 180)),
            # 优先级 - 放大
            draw_text_with_shadow(draw, (540, 1680), 
                "🔴必做：1-4 项   🟡建议：5-10 项", 
                get_font(28), (255, 255, 255)),
        ]
    )
    
    # ========== 07_summary: 行动呼吁 ==========
    process_image(
        os.path.join(INPUT_DIR, "07_summary.png"),
        os.path.join(OUTPUT_DIR, "07_summary.png"),
        lambda draw, size: [
            # 行动呼吁 - 白色 + 绿色箭头
            draw_text_with_shadow(draw, (540, 1550), 
                "👉 立即检查你的部署配置", 
                get_font(30), (255, 255, 255)),
        ]
    )
    
    print()
    print("=" * 60)
    print("排版优化 v4 完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
