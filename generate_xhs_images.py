#!/usr/bin/env uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow", "playwright"]
# ///

"""
OpenClaw 安全性分析 - 小红书图片生成器
使用 HTML/CSS + Playwright 生成小红书风格图片

色彩规范：
- 背景：#050505 (深黑)
- 强调红：#FF3333 (高饱和，带发光)
- 强调蓝：#3B82F6 (高饱和)
- 文字：#FFFFFF (主) / #E5E5E5 (次)

关键设计决策：
1. 封面图必须包含 OpenClaw Logo (SVG 嵌入)
2. 风险矩阵使用 CSS 圆点 + 发光效果，不用文本符号
3. 所有警示元素需带 box-shadow 发光增强可见度
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# 配置
OUTPUT_DIR = Path("02_内容项目/已发布/OpenClaw 安全性分析/fig/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 主题色 - 色彩丰富、富有设计感的新配色（更明亮的版本）
COLORS = {
    "bg": "#1a2744",              # 更亮的深蓝底色
    "bg_secondary": "#2d3e5f",     # 更亮的次级背景
    "bg_gradient_start": "#243452",
    "bg_gradient_end": "#354a6e",
    "accent_red": "#ff5e6e",       # 更亮的珊瑚红
    "accent_blue": "#4aa8ff",      # 更亮的蓝色
    "accent_purple": "#b57edc",    # 更亮的紫罗兰
    "accent_cyan": "#2de8ff",      # 更亮的青蓝色
    "accent_orange": "#ffb347",    # 更亮的橙色
    "accent_green": "#4ade80",     # 新增亮绿色
    "text_primary": "#ffffff",
    "text_secondary": "#c5d0e0",   # 更亮的次要文字
    "border": "#4a5a7a",           # 更亮的边框
    "glass_bg": "rgba(255,255,255,0.12)", # 更透明的玻璃态
    "glass_border": "rgba(255,255,255,0.25)" # 更亮的玻璃边框
}

# 图片配置
IMAGE_CONFIG = {
    "width": 1080,
    "height": 1920,  # 9:16 小红书标准比例
    "scale": 1  # 标准清晰度
}

# 色彩规范（更新为视觉规划要求的配色）
COLORS = {
    "bg": "#050505",              # 深黑背景
    "bg_secondary": "#0a0a0a",     # 次级背景
    "bg_gradient_start": "#050505",
    "bg_gradient_end": "#0d0d0d",
    "accent_red": "#FF3333",       # 高饱和暗红
    "accent_blue": "#3B82F6",      # 科技蓝
    "accent_purple": "#9333EA",    # 紫色
    "accent_cyan": "#06B6D4",      # 青色
    "accent_orange": "#F97316",    # 橙色
    "accent_green": "#10B981",     # 绿色
    "text_primary": "#FFFFFF",
    "text_secondary": "#E5E5E5",
    "border": "#374151",
    "glass_bg": "rgba(255,255,255,0.08)",
    "glass_border": "rgba(255,255,255,0.15)"
}


def generate_cover_html():
    """封面图 HTML - 暗黑科技风格（视觉规划 v1.1 精修版）"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: {IMAGE_CONFIG['width']}px;
            height: {IMAGE_CONFIG['height']}px;
            background: radial-gradient(circle at 50% 40%, #1a1a1a 0%, {COLORS['bg']} 60%, #000000 100%);
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 0;
            position: relative;
        }}
        /* 动态网格背景 */
        .grid-bg {{
            position: absolute;
            width: 100%;
            height: 100%;
            background-image:
                linear-gradient(rgba(74, 168, 255, 0.15) 1px, transparent 1px),
                linear-gradient(90deg, rgba(74, 168, 255, 0.15) 1px, transparent 1px);
            background-size: 60px 60px;
            z-index: 0;
        }}
        /* 装饰圆环 */
        .ring {{
            position: absolute;
            border-radius: 50%;
            border: 1px solid rgba(74, 168, 255, 0.4);
            z-index: 1;
        }}
        .ring-1 {{ width: 600px; height: 600px; top: -200px; right: -150px; opacity: 0.7; }}
        .ring-2 {{ width: 400px; height: 400px; bottom: 100px; left: -100px; opacity: 0.5; border-color: rgba(181, 126, 220, 0.4); }}
        .ring-3 {{ width: 300px; height: 300px; top: 300px; right: 50px; opacity: 0.4; border-color: rgba(45, 232, 255, 0.4); }}
        /* 渐变光斑 */
        .glow {{
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            z-index: 0;
        }}
        .glow-1 {{
            width: 450px; height: 450px;
            top: -120px; left: -120px;
            background: radial-gradient(circle, rgba(74, 168, 255, 0.5) 0%, transparent 70%);
        }}
        .glow-2 {{
            width: 400px; height: 400px;
            bottom: -80px; right: -80px;
            background: radial-gradient(circle, rgba(181, 126, 220, 0.4) 0%, transparent 70%);
        }}
        .glow-3 {{
            width: 300px; height: 300px;
            top: 40%; left: 50%;
            transform: translateX(-50%);
            background: radial-gradient(circle, rgba(255, 94, 110, 0.35) 0%, transparent 70%);
        }}
        /* 浮动几何图形 */
        .geo {{
            position: absolute;
            z-index: 1;
            opacity: 0.3;
        }}
        .geo-1 {{
            width: 80px; height: 80px;
            top: 150px; left: 60px;
            background: linear-gradient(135deg, {COLORS['accent_cyan']}, {COLORS['accent_blue']});
            border-radius: 20px;
            transform: rotate(15deg);
        }}
        .geo-2 {{
            width: 60px; height: 60px;
            bottom: 200px; right: 80px;
            background: linear-gradient(135deg, {COLORS['accent_purple']}, {COLORS['accent_red']});
            border-radius: 50%;
        }}
        .geo-3 {{
            width: 40px; height: 40px;
            top: 400px; right: 150px;
            background: linear-gradient(135deg, {COLORS['accent_orange']}, {COLORS['accent_red']});
            border-radius: 10px;
            transform: rotate(45deg);
        }}
        /* 角标 - 玻璃态风格 */
        .corner-badge {{
            position: absolute;
            top: 40px;
            right: 40px;
            background: {COLORS['glass_bg']};
            backdrop-filter: blur(10px);
            border: 1px solid {COLORS['glass_border']};
            color: {COLORS['accent_red']};
            padding: 12px 24px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 2px;
            z-index: 10;
            box-shadow: 0 8px 32px rgba(255, 71, 87, 0.2);
        }}
        /* Logo 容器 - 玻璃态 */
        .logo-container {{
            width: 220px;
            height: 220px;
            margin: 0 0 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: {COLORS['glass_bg']};
            backdrop-filter: blur(20px);
            border: 2px solid {COLORS['glass_border']};
            border-radius: 35px;
            z-index: 10;
            padding: 25px;
            box-shadow:
                0 25px 80px rgba(255, 51, 51, 0.25),
                inset 0 1px 0 rgba(255,255,255,0.1);
        }}
        .logo-svg svg {{
            width: 100%;
            height: 100%;
            filter: drop-shadow(0 0 30px {COLORS['accent_red']}99);
        }}
        .main-title {{
            font-size: 72px;
            font-weight: 800;
            color: {COLORS['text_primary']};
            text-align: center;
            margin-bottom: 15px;
            z-index: 10;
            line-height: 1.15;
            text-shadow: 0 4px 40px rgba(0,0,0,0.6);
            letter-spacing: 2px;
        }}
        .main-title .highlight {{
            color: {COLORS['accent_red']};
            background: linear-gradient(135deg, {COLORS['accent_red']}, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 40px rgba(255, 51, 51, 0.5);
        }}
        .sub-title {{
            font-size: 34px;
            color: {COLORS['text_secondary']};
            text-align: center;
            margin-bottom: 35px;
            line-height: 1.5;
            z-index: 10;
            text-shadow: 0 2px 20px rgba(0,0,0,0.5);
        }}
        .divider {{
            width: 180px;
            height: 4px;
            background: linear-gradient(90deg, transparent, {COLORS['accent_red']}, {COLORS['accent_blue']}, transparent);
            margin: 15px 0 30px;
            z-index: 10;
            border-radius: 2px;
            box-shadow: 0 0 20px rgba(255, 51, 51, 0.5);
        }}
        /* 标签 - 玻璃态 */
        .tags {{
            display: flex;
            gap: 14px;
            z-index: 10;
            flex-wrap: wrap;
            justify-content: center;
            max-width: 85%;
            margin-top: 10px;
        }}
        .tag {{
            background: {COLORS['glass_bg']};
            backdrop-filter: blur(10px);
            border: 1px solid {COLORS['glass_border']};
            color: {COLORS['text_primary']};
            padding: 12px 24px;
            border-radius: 22px;
            font-size: 16px;
            font-weight: 600;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .tag:nth-child(1) {{ border-color: rgba(59, 130, 246, 0.5); color: {COLORS['accent_blue']}; box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }}
        .tag:nth-child(2) {{ border-color: rgba(255, 51, 51, 0.5); color: {COLORS['accent_red']}; box-shadow: 0 0 20px rgba(255, 51, 51, 0.3); }}
        .tag:nth-child(3) {{ border-color: rgba(147, 51, 234, 0.5); color: {COLORS['accent_purple']}; box-shadow: 0 0 20px rgba(147, 51, 234, 0.3); }}
    </style>
</head>
<body>
    <!-- 背景光效 -->
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>
    <div class="glow glow-3"></div>
    <!-- 装饰圆环 -->
    <div class="ring ring-1"></div>
    <div class="ring ring-2"></div>

    <div class="corner-badge">AI 安全深度分析</div>

    <div class="logo-container">
        <div class="logo-svg">
            <!-- OpenClaw Logo SVG -->
            <svg viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="lobster-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#ff6b6b"/>
                        <stop offset="100%" stop-color="#ff4757"/>
                    </linearGradient>
                </defs>
                <path d="M60 10 C30 10 15 35 15 55 C15 75 30 95 45 100 L45 110 L55 110 L55 100 C55 100 60 102 65 100 L65 110 L75 110 L75 100 C90 95 105 75 105 55 C105 35 90 10 60 10Z" fill="url(#lobster-gradient)"/>
                <path d="M20 45 C5 40 0 50 5 60 C10 70 20 65 25 55 C28 48 25 45 20 45Z" fill="url(#lobster-gradient)"/>
                <path d="M100 45 C115 40 120 50 115 60 C110 70 100 65 95 55 C92 48 95 45 100 45Z" fill="url(#lobster-gradient)"/>
                <path d="M45 15 Q35 5 30 8" stroke="#ff6b6b" stroke-width="3" stroke-linecap="round"/>
                <path d="M75 15 Q85 5 90 8" stroke="#ff6b6b" stroke-width="3" stroke-linecap="round"/>
                <circle cx="45" cy="35" r="6" fill="#0a1628"/>
                <circle cx="75" cy="35" r="6" fill="#0a1628"/>
                <circle cx="46" cy="34" r="2.5" fill="#00d2ff"/>
                <circle cx="76" cy="34" r="2.5" fill="#00d2ff"/>
            </svg>
        </div>
    </div>

    <h1 class="main-title">OpenClaw <span class="highlight">突然火了</span></h1>

    <div class="divider"></div>

    <p class="sub-title">这些安全隐患你必须知道</p>

    <div class="tags">
        <div class="tag">#AI 安全</div>
        <div class="tag">#网络安全</div>
        <div class="tag">#漏洞分析</div>
    </div>
</body>
</html>
"""


def generate_architecture_html():
    """架构图 HTML - 暗黑科技风格（视觉规划 v1.1）"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: {IMAGE_CONFIG['width']}px;
            height: {IMAGE_CONFIG['height']}px;
            background: radial-gradient(circle at 50% 30%, #121212 0%, {COLORS['bg']} 70%, #000000 100%);
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            padding: 40px 50px;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }}
        /* 更亮的背景装饰 */
        .bg-pattern {{
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background-image:
                radial-gradient(circle at 25% 25%, rgba(74, 168, 255, 0.2) 0%, transparent 45%),
                radial-gradient(circle at 75% 75%, rgba(181, 126, 220, 0.18) 0%, transparent 45%);
            z-index: 0;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
            z-index: 1;
        }}
        .title {{
            font-size: 52px;
            font-weight: 800;
            color: {COLORS['text_primary']};
            margin-bottom: 8px;
            text-shadow: 0 4px 30px rgba(0,0,0,0.6);
            letter-spacing: 2px;
        }}
        .subtitle {{
            font-size: 22px;
            color: {COLORS['accent_blue']};
            font-weight: 600;
            letter-spacing: 1px;
            text-shadow: 0 2px 15px rgba(59, 130, 246, 0.4);
        }}
        .diagram {{
            flex: 1;
            background: {COLORS['glass_bg']};
            backdrop-filter: blur(20px);
            border-radius: 28px;
            padding: 35px 30px;
            border: 2px solid {COLORS['glass_border']};
            display: flex;
            flex-direction: column;
            gap: 18px;
            z-index: 1;
            box-shadow: 0 25px 80px rgba(0,0,0,0.4);
        }}
        .gateway-box {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(59, 130, 246, 0.1) 100%);
            border: 3px solid rgba(59, 130, 246, 0.6);
            border-radius: 24px;
            padding: 40px 30px;
            text-align: center;
            box-shadow: 0 15px 50px rgba(59, 130, 246, 0.3), inset 0 1px 0 rgba(255,255,255,0.1);
        }}
        .gateway-title {{
            font-size: 42px;
            font-weight: 800;
            color: {COLORS['text_primary']};
            margin-bottom: 12px;
            letter-spacing: 3px;
            text-shadow: 0 0 30px rgba(59, 130, 246, 0.5);
        }}
        .gateway-desc {{
            font-size: 20px;
            color: {COLORS['accent_blue']};
            font-weight: 600;
            text-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
        }}
        .arrow {{
            text-align: center;
            font-size: 36px;
            color: {COLORS['accent_cyan']};
            text-shadow: 0 0 25px rgba(6, 182, 212, 0.8);
            margin: 5px 0;
        }}
        .capabilities {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 14px;
        }}
        .cap-item {{
            background: rgba(255,255,255,0.06);
            border: 2px solid rgba(255,255,255,0.12);
            border-radius: 18px;
            padding: 18px 14px;
            display: flex;
            align-items: center;
            gap: 14px;
            transition: all 0.3s ease;
        }}
        .cap-icon {{
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, {COLORS['accent_red']}, {COLORS['accent_orange']});
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            box-shadow: 0 6px 25px rgba(255, 51, 51, 0.5);
            flex-shrink: 0;
        }}
        .cap-text {{
            font-size: 19px;
            color: {COLORS['text_primary']};
            font-weight: 600;
            line-height: 1.3;
        }}
        .warning-bar {{
            background: linear-gradient(90deg, rgba(255, 51, 51, 0.2) 0%, rgba(249, 115, 22, 0.15) 100%);
            border: 3px solid rgba(255, 51, 51, 0.7);
            border-radius: 18px;
            padding: 18px 16px;
            display: flex;
            align-items: center;
            gap: 16px;
            margin-top: 5px;
            box-shadow: 0 0 40px rgba(255, 51, 51, 0.35);
        }}
        .warning-icon {{
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, {COLORS['accent_red']}, {COLORS['accent_orange']});
            clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
            flex-shrink: 0;
            box-shadow: 0 0 25px rgba(255, 51, 51, 0.8);
        }}
        .warning-text {{
            font-size: 20px;
            color: {COLORS['accent_red']};
            font-weight: 700;
            letter-spacing: 1px;
            text-shadow: 0 0 20px rgba(255, 51, 51, 0.5);
        }}
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    <div class="header">
        <h1 class="title">OpenClaw 架构解析</h1>
        <p class="subtitle">Gateway + Node 架构</p>
    </div>

    <div class="diagram">
        <div class="gateway-box">
            <div class="gateway-title">Gateway</div>
            <div class="gateway-desc">本地服务 - 端口 18789</div>
        </div>

        <div class="arrow">▼</div>

        <div class="capabilities">
            <div class="cap-item">
                <div class="cap-icon">1</div>
                <div class="cap-text">终端命令执行</div>
            </div>
            <div class="cap-item">
                <div class="cap-icon">2</div>
                <div class="cap-text">文件系统读写</div>
            </div>
            <div class="cap-item">
                <div class="cap-icon">3</div>
                <div class="cap-text">浏览器控制</div>
            </div>
            <div class="cap-item">
                <div class="cap-icon">4</div>
                <div class="cap-text">摄像头/麦克风</div>
            </div>
            <div class="cap-item">
                <div class="cap-icon">5</div>
                <div class="cap-text">剪贴板/定位</div>
            </div>
            <div class="cap-item">
                <div class="cap-icon">6</div>
                <div class="cap-text">多渠道集成</div>
            </div>
        </div>

        <div class="warning-bar">
            <div class="warning-icon"></div>
            <div class="warning-text">沙箱默认关闭 = 宿主机直接执行</div>
        </div>
    </div>
</body>
</html>
"""


def generate_timeline_html():
    """时间线 HTML - 色彩丰富版"""
    events = [
        {"date": "2026.01", "title": "RCE 漏洞修复", "desc": "CVE-2026-25253 等高危漏洞", "color": "blue"},
        {"date": "2026.02.09", "title": "4.3 万实例暴露", "desc": "1.5 万存在 RCE 漏洞", "color": "purple"},
        {"date": "2026.02.19", "title": "ClawHub 供应链危机", "desc": "1184 个欺诈技能被发现", "color": "orange"},
        {"date": "2026.02.25", "title": "ClawJacked 漏洞披露", "desc": "任意网站可暴力破解本地代理", "color": "red"},
    ]

    event_items = "".join([
        f"""
        <div class="event-item">
            <div class="event-icon {e['color']}"></div>
            <div class="event-content">
                <div class="event-date">{e['date']}</div>
                <div class="event-title">{e['title']}</div>
                <div class="event-desc">{e['desc']}</div>
            </div>
        </div>
        """ for i, e in enumerate(events)
    ])

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: {IMAGE_CONFIG['width']}px;
            height: {IMAGE_CONFIG['height']}px;
            background: linear-gradient(180deg, {COLORS['bg']} 0%, {COLORS['bg_secondary']} 100%);
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            padding: 50px 60px;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }}
        /* 更亮的背景装饰 */
        .bg-glow {{
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background:
                radial-gradient(circle at 10% 20%, rgba(74, 168, 255, 0.18) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(255, 94, 110, 0.15) 0%, transparent 40%);
            z-index: 0;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            z-index: 1;
        }}
        .title {{
            font-size: 40px;
            font-weight: 700;
            color: {COLORS['text_primary']};
        }}
        .timeline {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 18px;
            z-index: 1;
        }}
        .event-item {{
            display: flex;
            align-items: flex-start;
            gap: 18px;
            padding: 22px;
            background: {COLORS['glass_bg']};
            backdrop-filter: blur(10px);
            border: 1px solid {COLORS['glass_border']};
            border-radius: 16px;
            transition: all 0.3s ease;
        }}
        .event-icon {{
            width: 50px;
            height: 50px;
            border-radius: 12px;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}
        .event-icon.blue {{
            background: linear-gradient(135deg, {COLORS['accent_blue']}, #5dade2);
            box-shadow: 0 8px 25px rgba(52, 152, 219, 0.4);
        }}
        .event-icon.purple {{
            background: linear-gradient(135deg, {COLORS['accent_purple']}, #bb8fce);
            box-shadow: 0 8px 25px rgba(155, 89, 182, 0.4);
        }}
        .event-icon.orange {{
            background: linear-gradient(135deg, {COLORS['accent_orange']}, #f8b500);
            box-shadow: 0 8px 25px rgba(255, 159, 67, 0.4);
        }}
        .event-icon.red {{
            background: linear-gradient(135deg, {COLORS['accent_red']}, #ff6b6b);
            box-shadow: 0 8px 25px rgba(255, 71, 87, 0.5);
        }}
        .event-content {{
            flex: 1;
        }}
        .event-date {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        .event-item:nth-child(1) .event-date {{ color: {COLORS['accent_blue']}; }}
        .event-item:nth-child(2) .event-date {{ color: {COLORS['accent_purple']}; }}
        .event-item:nth-child(3) .event-date {{ color: {COLORS['accent_orange']}; }}
        .event-item:nth-child(4) .event-date {{ color: {COLORS['accent_red']}; }}
        .event-title {{
            font-size: 22px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            margin-bottom: 6px;
        }}
        .event-desc {{
            font-size: 14px;
            color: {COLORS['text_secondary']};
            line-height: 1.4;
        }}
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="header">
        <h1 class="title">安全事件时间线</h1>
    </div>

    <div class="timeline">
        {event_items}
    </div>
</body>
</html>
"""


def generate_attack_flow_html():
    """攻击路径流程图 HTML - 色彩丰富版"""
    steps = [
        {"num": 1, "title": "用户浏览网页", "desc": "正常使用浏览器访问网站", "color": "blue"},
        {"num": 2, "title": "误入钓鱼网站", "desc": "被诱导访问恶意网页", "color": "cyan"},
        {"num": 3, "title": "JS 连接 localhost:18789", "desc": "网页 JavaScript 尝试本地 WebSocket 连接", "color": "purple"},
        {"num": 4, "title": "暴力破解密码", "desc": "本地连接不受失败限速限制", "color": "orange"},
        {"num": 5, "title": "注册为受信设备", "desc": "成功通过身份验证", "color": "red"},
        {"num": 6, "title": "完全接管代理", "desc": "执行任意命令/读取文件/访问日志", "color": "red"},
    ]

    step_items = "".join([
        f"""
        <div class="step-item {s['color']}">
            <div class="step-number">{s['num']}</div>
            <div class="step-content">
                <div class="step-title">{s['title']}</div>
                <div class="step-desc">{s['desc']}</div>
            </div>
        </div>
        """ for i, s in enumerate(steps)
    ])

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: {IMAGE_CONFIG['width']}px;
            height: {IMAGE_CONFIG['height']}px;
            background: linear-gradient(180deg, {COLORS['bg']} 0%, {COLORS['bg_secondary']} 100%);
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            padding: 45px 60px;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }}
        /* 更亮的背景装饰 */
        .bg-decor {{
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background:
                radial-gradient(circle at 80% 20%, rgba(74, 168, 255, 0.15) 0%, transparent 35%),
                radial-gradient(circle at 20% 80%, rgba(255, 94, 110, 0.18) 0%, transparent 40%);
            z-index: 0;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            z-index: 1;
        }}
        .title {{
            font-size: 36px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            margin-bottom: 8px;
        }}
        .subtitle {{
            font-size: 16px;
            color: {COLORS['text_secondary']};
        }}
        .cvss-badge {{
            position: absolute;
            top: 40px;
            right: 40px;
            background: linear-gradient(135deg, {COLORS['accent_red']}, {COLORS['accent_orange']});
            color: {COLORS['text_primary']};
            padding: 14px 22px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(255, 71, 87, 0.4);
            z-index: 10;
        }}
        .cvss-score {{
            font-size: 32px;
            font-weight: 800;
        }}
        .cvss-label {{
            font-size: 13px;
            opacity: 0.9;
            font-weight: 500;
        }}
        .flow-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 12px;
            overflow: hidden;
            z-index: 1;
        }}
        .step-item {{
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 14px 18px;
            background: {COLORS['glass_bg']};
            backdrop-filter: blur(10px);
            border: 1px solid {COLORS['glass_border']};
            border-radius: 14px;
            transition: all 0.3s ease;
        }}
        .step-number {{
            width: 42px;
            height: 42px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            flex-shrink: 0;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        /* 不同颜色的步骤 */
        .step-item.blue {{ border-left: 4px solid {COLORS['accent_blue']}; }}
        .step-item.blue .step-number {{ background: linear-gradient(135deg, {COLORS['accent_blue']}, #5dade2); box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4); }}

        .step-item.cyan {{ border-left: 4px solid {COLORS['accent_cyan']}; }}
        .step-item.cyan .step-number {{ background: linear-gradient(135deg, {COLORS['accent_cyan']}, #5dade2); box-shadow: 0 6px 20px rgba(0, 210, 255, 0.4); }}

        .step-item.purple {{ border-left: 4px solid {COLORS['accent_purple']}; }}
        .step-item.purple .step-number {{ background: linear-gradient(135deg, {COLORS['accent_purple']}, #bb8fce); box-shadow: 0 6px 20px rgba(155, 89, 182, 0.4); }}

        .step-item.orange {{ border-left: 4px solid {COLORS['accent_orange']}; }}
        .step-item.orange .step-number {{ background: linear-gradient(135deg, {COLORS['accent_orange']}, #f8b500); box-shadow: 0 6px 20px rgba(255, 159, 67, 0.4); }}

        .step-item.red {{ border-left: 4px solid {COLORS['accent_red']}; background: rgba(255, 71, 87, 0.08); }}
        .step-item.red .step-number {{ background: linear-gradient(135deg, {COLORS['accent_red']}, #ff6b6b); box-shadow: 0 6px 20px rgba(255, 71, 87, 0.5); }}

        .step-content {{
            flex: 1;
        }}
        .step-title {{
            font-size: 18px;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin-bottom: 4px;
        }}
        .step-desc {{
            font-size: 13px;
            color: {COLORS['text_secondary']};
        }}
    </style>
</head>
<body>
    <div class="bg-decor"></div>
    <div class="header">
        <h1 class="title">ClawJacked 攻击路径</h1>
        <p class="subtitle">CVE-2026-25253 漏洞利用链</p>
    </div>

    <div class="cvss-badge">
        <div class="cvss-score">8.8</div>
        <div class="cvss-label">CVSS 高危</div>
    </div>

    <div class="flow-container">
        {step_items}
    </div>
</body>
</html>
"""


def generate_risk_matrix_html():
    """风险评估 HTML - 卡片式风险对比"""
    risks = [
        {"name": "核心平台漏洞", "user": 3.5, "dev": 3.5, "enterprise": 4, "icon": "⚠️"},
        {"name": "供应链风险", "user": 2, "dev": 4, "enterprise": 3.5, "icon": "📦"},
        {"name": "分发伪装", "user": 4, "dev": 3, "enterprise": 3, "icon": "🎭"},
        {"name": "部署配置", "user": 2, "dev": 3, "enterprise": 4, "icon": "⚙️"},
        {"name": "权限滥用", "user": 3.5, "dev": 3.5, "enterprise": 4, "icon": "🔑"},
    ]

    colors = {
        "user": COLORS['accent_blue'],
        "dev": COLORS['accent_purple'],
        "enterprise": COLORS['accent_red']
    }

    def get_risk_bar(rating, color):
        percentage = (rating / 4) * 100
        return f'''
        <div class="risk-bar-container">
            <div class="risk-bar-bg"></div>
            <div class="risk-bar-fill" style="width: {percentage}%; background: linear-gradient(90deg, {color}, {color}aa);"></div>
        </div>
        '''

    def get_risk_level(rating):
        if rating >= 3.5:
            return "极高"
        elif rating >= 2.5:
            return "高"
        elif rating >= 1.5:
            return "中"
        else:
            return "低"

    risk_cards = ""
    for i, r in enumerate(risks):
        risk_cards += f"""
        <div class="risk-card">
            <div class="risk-header">
                <span class="risk-icon">{r['icon']}</span>
                <span class="risk-name">{r['name']}</span>
            </div>
            <div class="risk-bars">
                <div class="risk-row">
                    <span class="row-label">普通用户</span>
                    {get_risk_bar(r['user'], colors['user'])}
                    <span class="row-value" style="color: {colors['user']}">{get_risk_level(r['user'])}</span>
                </div>
                <div class="risk-row">
                    <span class="row-label">开发者</span>
                    {get_risk_bar(r['dev'], colors['dev'])}
                    <span class="row-value" style="color: {colors['dev']}">{get_risk_level(r['dev'])}</span>
                </div>
                <div class="risk-row">
                    <span class="row-label">企业</span>
                    {get_risk_bar(r['enterprise'], colors['enterprise'])}
                    <span class="row-value" style="color: {colors['enterprise']}">{get_risk_level(r['enterprise'])}</span>
                </div>
            </div>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: {IMAGE_CONFIG['width']}px;
            height: 1920px;
            background: linear-gradient(180deg, {COLORS['bg']} 0%, {COLORS['bg_secondary']} 100%);
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            padding: 50px 60px;
            position: relative;
            overflow: hidden;
        }}
        /* 更亮的背景装饰 */
        .bg-decor {{
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background:
                radial-gradient(circle at 20% 20%, rgba(74, 168, 255, 0.18) 0%, transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(255, 94, 110, 0.15) 0%, transparent 40%);
            z-index: 0;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            z-index: 1;
        }}
        .title {{
            font-size: 48px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            margin-bottom: 12px;
        }}
        .subtitle {{
            font-size: 20px;
            color: {COLORS['text_secondary']};
        }}
        .legend {{
            display: flex;
            justify-content: center;
            gap: 35px;
            margin-bottom: 35px;
            z-index: 1;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 18px;
            color: {COLORS['text_secondary']};
        }}
        .legend-dot {{
            width: 16px;
            height: 16px;
            border-radius: 50%;
        }}
        .cards-container {{
            display: flex;
            flex-direction: column;
            gap: 20px;
            z-index: 1;
            width: 100%;
        }}
        .risk-card {{
            background: {COLORS['glass_bg']};
            backdrop-filter: blur(15px);
            border: 1px solid {COLORS['glass_border']};
            border-radius: 20px;
            padding: 24px 28px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }}
        .risk-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 18px;
        }}
        .risk-icon {{
            font-size: 26px;
        }}
        .risk-name {{
            font-size: 22px;
            font-weight: 700;
            color: {COLORS['text_primary']};
        }}
        .risk-bars {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        .risk-row {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}
        .row-label {{
            width: 90px;
            font-size: 16px;
            color: {COLORS['text_secondary']};
            text-align: right;
        }}
        .risk-bar-container {{
            flex: 1;
            height: 12px;
            position: relative;
            border-radius: 6px;
        }}
        .risk-bar-bg {{
            position: absolute;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.1);
            border-radius: 6px;
        }}
        .risk-bar-fill {{
            position: absolute;
            height: 100%;
            border-radius: 6px;
            transition: width 0.5s ease;
        }}
        .row-value {{
            width: 50px;
            font-size: 15px;
            font-weight: 700;
            text-align: left;
        }}
    </style>
</head>
<body>
    <div class="bg-decor"></div>
    <div class="header">
        <h1 class="title">风险评估矩阵</h1>
        <p class="subtitle">不同用户群体面临的风险等级</p>
    </div>

    <div class="legend">
        <div class="legend-item">
            <div class="legend-dot" style="background: {COLORS['accent_blue']}"></div>
            <span>普通用户</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: {COLORS['accent_purple']}"></div>
            <span>开发者</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background: {COLORS['accent_red']}"></div>
            <span>企业</span>
        </div>
    </div>

    <div class="cards-container">
        {risk_cards}
    </div>
</body>
</html>
"""


def generate_checklist_html():
    """防护清单 HTML - 色彩丰富版（优化布局）"""
    items = [
        {"text": "只从官网/GitHub 官方下载安装", "icon": "shield"},
        {"text": "更新至最新版本 (2026.2.25+)", "icon": "sync"},
        {"text": "只监听 127.0.0.1:18789", "icon": "network"},
        {"text": "不暴露公网", "icon": "lock"},
        {"text": "在虚拟机/容器中运行", "icon": "box"},
        {"text": "不以管理员身份运行", "icon": "user"},
        {"text": "仅与可信联系人配对", "icon": "check"},
        {"text": "群聊启用@提及策略", "icon": "at"},
        {"text": "只安装可信开发者技能", "icon": "code"},
        {"text": "不存储敏感凭证在配置中", "icon": "key"},
    ]

    checklist_items = "".join([
        f"""
        <div class="checklist-item">
            <div class="checkbox {item['icon']}"></div>
            <div class="item-text">{item['text']}</div>
        </div>
        """ for item in items
    ])

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: {IMAGE_CONFIG['width']}px;
            height: 1920px;
            background: linear-gradient(180deg, {COLORS['bg']} 0%, {COLORS['bg_secondary']} 100%);
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            padding: 50px 60px;
            position: relative;
            overflow: hidden;
        }}
        /* 更亮的背景装饰 */
        .bg-decor {{
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background:
                radial-gradient(circle at 15% 20%, rgba(45, 232, 255, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 85% 80%, rgba(74, 168, 255, 0.12) 0%, transparent 40%);
            z-index: 0;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            z-index: 1;
        }}
        .title {{
            font-size: 48px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            margin-bottom: 12px;
        }}
        .subtitle {{
            font-size: 20px;
            color: {COLORS['accent_cyan']};
            font-weight: 600;
        }}
        .checklist-container {{
            background: {COLORS['glass_bg']};
            backdrop-filter: blur(20px);
            border: 1px solid {COLORS['glass_border']};
            border-radius: 24px;
            padding: 30px;
            overflow: hidden;
            z-index: 1;
            box-shadow: 0 20px 60px rgba(0,0,0,0.25);
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(5, 1fr);
            gap: 18px;
            width: 100%;
            height: 1680px;
        }}
        .checklist-item {{
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 16px 18px;
            background: rgba(255,255,255,0.06);
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.12);
            transition: all 0.3s ease;
        }}
        .checkbox {{
            width: 28px;
            height: 28px;
            border-radius: 8px;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: white;
            font-weight: 700;
        }}
        .item-text {{
            font-size: 18px;
            color: {COLORS['text_primary']};
            font-weight: 500;
            line-height: 1.4;
        }}
        .checklist-item:hover {{
            background: rgba(255,255,255,0.1);
            transform: translateX(5px);
        }}
        .checkbox {{
            width: 32px;
            height: 32px;
            border-radius: 10px;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            color: white;
            font-weight: 700;
        }}
        .checkbox.shield {{ background: linear-gradient(135deg, #4aa8ff, #74c0ff); box-shadow: 0 4px 16px rgba(74, 168, 255, 0.5); }}
        .checkbox.sync {{ background: linear-gradient(135deg, #b57edc, #d4a5f0); box-shadow: 0 4px 16px rgba(181, 126, 220, 0.5); }}
        .checkbox.network {{ background: linear-gradient(135deg, #2de8ff, #74f0ff); box-shadow: 0 4px 16px rgba(45, 232, 255, 0.5); }}
        .checkbox.lock {{ background: linear-gradient(135deg, #ff5e6e, #ff8a9a); box-shadow: 0 4px 16px rgba(255, 94, 110, 0.5); }}
        .checkbox.box {{ background: linear-gradient(135deg, #ffb347, #ffd180); box-shadow: 0 4px 16px rgba(255, 179, 71, 0.5); }}
        .checkbox.user {{ background: linear-gradient(135deg, #58e0ff, #8aeaff); box-shadow: 0 4px 16px rgba(88, 224, 255, 0.5); }}
        .checkbox.check {{ background: linear-gradient(135deg, #4ade80, #6ee8a0); box-shadow: 0 4px 16px rgba(74, 222, 128, 0.5); }}
        .checkbox.at {{ background: linear-gradient(135deg, #7c5cff, #a080ff); box-shadow: 0 4px 16px rgba(124, 92, 255, 0.5); }}
        .checkbox.code {{ background: linear-gradient(135deg, #ff7a8a, #ff5e6e); box-shadow: 0 4px 16px rgba(255, 122, 138, 0.5); }}
        .checkbox.key {{ background: linear-gradient(135deg, #ffd166, #ffe0a0); box-shadow: 0 4px 16px rgba(255, 209, 102, 0.5); }}

        .item-text {{
            font-size: 19px;
            color: {COLORS['text_primary']};
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <div class="bg-decor"></div>
    <div class="header">
        <h1 class="title">防护清单</h1>
        <p class="subtitle">正在使用的人必看</p>
    </div>

    <div class="checklist-container">
        {checklist_items}
    </div>
</body>
</html>
"""


def generate_summary_html():
    """核心论点总结 HTML - 色彩丰富版"""
    points = [
        {"text": "OpenClaw 不是普通聊天 AI，是操作系统级代理", "color": "blue"},
        {"text": "官方信任模型仅限个人使用，不支持多人共享", "color": "purple"},
        {"text": "ClawHub 供应链存在严重后门风险 (1184 个欺诈技能)", "color": "orange"},
        {"text": "ClawJacked 证明过度信任本地是隐患", "color": "red"},
        {"text": "默认配置是安全隐患 (上万实例暴露公网)", "color": "cyan"},
        {"text": "防护基石是最小权限和隔离", "color": "green"},
    ]

    summary_points = "".join([
        f"""
        <div class="point-item">
            <div class="point-number {p['color']}">{i+1}</div>
            <div class="point-text">{p['text']}</div>
        </div>
        """ for i, p in enumerate(points)
    ])

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: {IMAGE_CONFIG['width']}px;
            height: {IMAGE_CONFIG['height']}px;
            background: linear-gradient(180deg, {COLORS['bg']} 0%, {COLORS['bg_secondary']} 100%);
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            padding: 50px 60px;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }}
        /* 更亮的背景装饰 */
        .bg-decor {{
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background:
                radial-gradient(circle at 20% 10%, rgba(74, 168, 255, 0.15) 0%, transparent 35%),
                radial-gradient(circle at 80% 90%, rgba(255, 94, 110, 0.12) 0%, transparent 40%);
            z-index: 0;
        }}
        .header {{
            text-align: center;
            margin-bottom: 25px;
            z-index: 1;
        }}
        .title {{
            font-size: 40px;
            font-weight: 700;
            color: {COLORS['text_primary']};
        }}
        .points-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 12px;
            overflow: hidden;
            z-index: 1;
        }}
        .point-item {{
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 16px 20px;
            background: {COLORS['glass_bg']};
            backdrop-filter: blur(10px);
            border: 1px solid {COLORS['glass_border']};
            border-radius: 14px;
            transition: all 0.3s ease;
        }}
        .point-number {{
            width: 38px;
            height: 38px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            flex-shrink: 0;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        .point-number.blue {{ background: linear-gradient(135deg, {COLORS['accent_blue']}, #5dade2); box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4); }}
        .point-number.purple {{ background: linear-gradient(135deg, {COLORS['accent_purple']}, #bb8fce); box-shadow: 0 6px 20px rgba(155, 89, 182, 0.4); }}
        .point-number.orange {{ background: linear-gradient(135deg, {COLORS['accent_orange']}, #f8b500); box-shadow: 0 6px 20px rgba(255, 159, 67, 0.4); }}
        .point-number.red {{ background: linear-gradient(135deg, {COLORS['accent_red']}, #ff6b6b); box-shadow: 0 6px 20px rgba(255, 71, 87, 0.5); }}
        .point-number.cyan {{ background: linear-gradient(135deg, {COLORS['accent_cyan']}, #5dade2); box-shadow: 0 6px 20px rgba(0, 210, 255, 0.4); }}
        .point-number.green {{ background: linear-gradient(135deg, #1dd1a1, #10ac84); box-shadow: 0 6px 20px rgba(29, 209, 161, 0.4); }}

        .point-text {{
            font-size: 16px;
            color: {COLORS['text_primary']};
            line-height: 1.5;
            flex: 1;
            font-weight: 500;
        }}
        .golden-quote {{
            margin-top: 25px;
            padding: 22px 30px;
            background: linear-gradient(135deg, rgba(255, 71, 87, 0.15) 0%, rgba(52, 152, 219, 0.1) 100%);
            border: 2px solid rgba(255, 71, 87, 0.3);
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(255, 71, 87, 0.15);
            z-index: 1;
        }}
        .quote-text {{
            font-size: 26px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            line-height: 1.5;
        }}
        .quote-text .highlight {{
            background: linear-gradient(135deg, {COLORS['accent_red']}, {COLORS['accent_orange']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
    </style>
</head>
<body>
    <div class="bg-decor"></div>
    <div class="header">
        <h1 class="title">核心论点总结</h1>
    </div>

    <div class="points-container">
        {summary_points}
    </div>

    <div class="golden-quote">
        <div class="quote-text">
            <span class="highlight">功能即风险边界</span><br>
            越像操作系统的工具，越需要专业部署
        </div>
    </div>
</body>
</html>
"""


async def main():
    """主函数：生成所有图片"""

    images = [
        ("01_cover.png", "封面", generate_cover_html()),
        ("02_architecture.png", "架构图", generate_architecture_html()),
        ("03_timeline.png", "时间线", generate_timeline_html()),
        ("04_attack_flow.png", "攻击路径", generate_attack_flow_html()),
        ("05_risk_matrix.png", "风险矩阵", generate_risk_matrix_html()),
        ("06_checklist.png", "防护清单", generate_checklist_html()),
        ("07_summary.png", "核心论点", generate_summary_html()),
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for filename, desc, html in images:
            print(f"正在生成：{desc} ({filename})...")

            page = await browser.new_page()
            await page.set_content(html, wait_until="networkidle")

            # 等待字体加载
            await page.wait_for_timeout(500)

            output_path = OUTPUT_DIR / filename

            # 获取页面实际高度
            content_height = await page.evaluate("document.documentElement.scrollHeight")
            # 使用固定高度 1920px（小红书 3:4 标准比例）
            screenshot_height = IMAGE_CONFIG['height']

            # 调整视口大小以匹配内容
            await page.set_viewport_size({
                "width": IMAGE_CONFIG['width'],
                "height": screenshot_height
            })

            await page.screenshot(
                path=str(output_path),
                full_page=False,
                clip={"x": 0, "y": 0, "width": IMAGE_CONFIG['width'], "height": screenshot_height}
            )

            await page.close()
            print(f"  [OK] 已保存：{output_path}")

        await browser.close()

    print("\n[SUCCESS] 所有图片生成完成！")


if __name__ == "__main__":
    asyncio.run(main())
