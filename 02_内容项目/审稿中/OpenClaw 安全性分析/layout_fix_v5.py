"""
OpenClaw 安全性分析图像排版优化脚本 v5 - 终极版
目标：留白≤40%，文字充实，视觉饱满
"""

from PIL import Image, ImageDraw, ImageFont
import os

INPUT_DIR = r"C:\Users\pnn\Desktop\socialmedia-work-studio\02_内容项目\审稿中\OpenClaw 安全性分析\fig\output"
OUTPUT_DIR = r"C:\Users\pnn\Desktop\socialmedia-work-studio\02_内容项目\审稿中\OpenClaw 安全性分析\fig\optimized"

def get_font(size):
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
    ]
    for fp in font_paths:
        try:
            return ImageFont.truetype(fp, size)
        except:
            continue
    return ImageFont.load_default()

def draw_shadow_text(draw, pos, text, font, color):
    x, y = pos
    draw.text((x+2, y+2), text, fill=(0,0,0,200), font=font)
    draw.text((x, y), text, fill=color, font=font)

def process(img_file, draw_func):
    img = Image.open(os.path.join(INPUT_DIR, img_file)).convert("RGBA")
    draw = ImageDraw.Draw(img)
    draw_func(draw, img.size)
    img.save(os.path.join(OUTPUT_DIR, img_file), "PNG", optimize=True)
    print(f"[OK] {img_file}")

def main():
    print("="*60)
    print("OpenClaw 安全性分析 - 终极优化 v5")
    print("="*60)
    
    # ========== 01_cover: 居中 + 核心要点 ==========
    process("01_cover.png", lambda draw, size: [
        # 引言 - 居中放大
        draw_shadow_text(draw, (540, 650), 
            "27 万星标的开源项目，背后藏着怎样的安全隐患？", 
            get_font(36), (255,255,255)),
        draw_shadow_text(draw, (540, 700), 
            "从 RCE 漏洞到 ClawJacked 攻击，深度解析 AI 代理的安全边界", 
            get_font(30), (230,230,230)),
        # 核心要点
        draw_shadow_text(draw, (540, 800), "🔍 核心看点", get_font(28), (100,200,255)),
        draw_shadow_text(draw, (540, 850), "• 4 起重大安全事件时间线", get_font(26), (240,240,240)),
        draw_shadow_text(draw, (540, 890), "• ClawJacked 攻击路径完整解析", get_font(26), (240,240,240)),
        draw_shadow_text(draw, (540, 930), "• 5 类风险评估矩阵", get_font(26), (240,240,240)),
        draw_shadow_text(draw, (540, 970), "• 10 条防护清单", get_font(26), (240,240,240)),
        # 底部引导
        draw_shadow_text(draw, (540, 1650), "⬇️ 下滑查看完整分析 ⬇️", get_font(40), (255,80,80)),
    ])
    
    # ========== 02_architecture: 紧接架构 + 风险列表 ==========
    process("02_architecture.png", lambda draw, size: [
        # 紧接架构图
        draw_shadow_text(draw, (540, 880), 
            "Gateway 作为中枢，直接调用系统 API", 
            get_font(30), (255,255,255)),
        draw_shadow_text(draw, (540, 920), 
            "沙箱关闭 = 所有命令在宿主机直接执行", 
            get_font(28), (255,100,100)),
        # 风险列表
        draw_shadow_text(draw, (540, 1000), "⚠️ 潜在风险", get_font(28), (255,150,50)),
        draw_shadow_text(draw, (540, 1050), "• 任意代码执行 - 攻击者可运行系统命令", get_font(24), (230,230,230)),
        draw_shadow_text(draw, (540, 1090), "• 文件读写 - 可窃取/篡改你的文档", get_font(24), (230,230,230)),
        draw_shadow_text(draw, (540, 1130), "• 隐私泄露 - 摄像头/麦克风/剪贴板无保护", get_font(24), (230,230,230)),
        draw_shadow_text(draw, (540, 1170), "• 凭证窃取 - API 密钥/密码可能被获取", get_font(24), (230,230,230)),
    ])
    
    # ========== 03_timeline: 添加洞察 ==========
    process("03_timeline.png", lambda draw, size: [
        # 总结条上移
        draw_shadow_text(draw, (540, 780), 
            "⚠️ 3 个月内 4 起重大安全事件", 
            get_font(32), (255,80,80)),
        # 安全洞察
        draw_shadow_text(draw, (540, 860), "📈 安全趋势分析", get_font(28), (100,200,255)),
        draw_shadow_text(draw, (540, 910), "• 漏洞发现频率：平均每 2 周 1 起", get_font(24), (230,230,230)),
        draw_shadow_text(draw, (540, 950), "• 影响范围：从 RCE 到供应链到本地接管", get_font(24), (230,230,230)),
        draw_shadow_text(draw, (540, 990), "• 攻击门槛：从技术专家→任意网站", get_font(24), (230,230,230)),
        draw_shadow_text(draw, (540, 1030), "• 风险等级：持续升级中", get_font(24), (255,100,100)),
    ])
    
    # ========== 04_attack_flow: 完整防护清单 ==========
    process("04_attack_flow.png", lambda draw, size: [
        # 防护建议 - 完整清单
        draw_shadow_text(draw, (540, 1300), "🛡️ 完整防护清单", get_font(32), (100,255,150)),
        draw_shadow_text(draw, (540, 1360), "1. 禁用 WebSocket 连接本地代理", get_font(26), (255,255,255)),
        draw_shadow_text(draw, (540, 1400), "2. 设置强密码（16 位 + 特殊字符）", get_font(26), (255,255,255)),
        draw_shadow_text(draw, (540, 1440), "3. 仅监听 127.0.0.1，不暴露公网", get_font(26), (255,255,255)),
        draw_shadow_text(draw, (540, 1480), "4. 使用防火墙限制入站连接", get_font(26), (255,255,255)),
        draw_shadow_text(draw, (540, 1520), "5. 定期审计日志，监控异常行为", get_font(26), (255,255,255)),
        draw_shadow_text(draw, (540, 1560), "6. 在虚拟机/容器中运行 OpenClaw", get_font(26), (255,255,255)),
    ])
    
    # ========== 05_risk_matrix: 详细解读 ==========
    process("05_risk_matrix.png", lambda draw, size: [
        # 详细解读
        draw_shadow_text(draw, (540, 1500), "📊 风险评估解读", get_font(30), (100,200,255)),
        draw_shadow_text(draw, (540, 1550), "核心平台漏洞：所有用户均面临极高风险", get_font(24), (255,255,255)),
        draw_shadow_text(draw, (540, 1590), "供应链风险：开发者/企业需格外警惕", get_font(24), (255,255,255)),
        draw_shadow_text(draw, (540, 1630), "分发伪装：普通用户最易中招", get_font(24), (255,255,255)),
        draw_shadow_text(draw, (540, 1670), "💡 建议：企业用户立即部署专业防护方案", get_font(26), (255,150,50)),
    ])
    
    # ========== 06_checklist: 字体加大 ==========
    process("06_checklist.png", lambda draw, size: [
        # 分类标题 - 加大
        draw_shadow_text(draw, (270, 70), "【安装部署】", get_font(28), (200,200,200)),
        draw_shadow_text(draw, (810, 70), "【权限管理】", get_font(28), (200,200,200)),
        draw_shadow_text(draw, (270, 470), "【日常使用】", get_font(28), (200,200,200)),
        # 方格内文字 - 加大
        # (原文字已存在，此处不重复绘制)
        # 优先级 - 加大
        draw_shadow_text(draw, (540, 1680), 
            "🔴必做：1-4 项   🟡建议：5-10 项", 
            get_font(32), (255,255,255)),
    ])
    
    # ========== 07_summary: 添加行动呼吁（金句已在原图底部） ==========
    process("07_summary.png", lambda draw, size: [
        # 行动呼吁
        draw_shadow_text(draw, (540, 1550), 
            "👉 立即检查你的部署配置", 
            get_font(32), (255,255,255)),
        draw_shadow_text(draw, (540, 1600), 
            "最小权限 + 隔离运行 = 安全基石", 
            get_font(28), (150,255,150)),
    ])
    
    print()
    print("="*60)
    print("终极优化 v5 完成！")
    print("="*60)

if __name__ == "__main__":
    main()
