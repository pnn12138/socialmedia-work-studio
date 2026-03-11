# OpenClaw 安全性分析 - 视觉规划与执行全案

**选题名称**：OpenClaw 安全性分析
**创建时间**：2026-03-10
**当前状态**：✅ 精修版规划完成，等待 visual-post-builder 执行

---

## 一、视觉策略总览

### 主题摘要
- **核心主题**：OpenClaw 突然火了，但这些安全隐患你必须知道
- **核心立场**：功能即风险边界，越像操作系统的工具越需要专业部署
- **封面抓手**：OpenClaw Logo + 安全警示视觉
- **视觉语气**：警示、审慎、专业，避免过度恐慌或通用素材感
- **关键词**：AI 安全、漏洞分析、风险警示、技术深度

### 视觉总原则
- **调性**：暗黑科技风，信息图优先
- **主色**：深黑 (#050505)、暗红 (#FF3333)
- **辅色**：科技蓝 (#3B82F6)、灰色 (#6B7280)、白色 (#FFFFFF)
- **禁止风格**：通用 Pexels 素材感、廉价 AI 发光图、与主题无关的氛围图
- **统一性要求**：所有图片保持深色主题，OpenClaw Logo 作为核心视觉元素贯穿
- **对比度要求**：文字与背景对比度≥7:1，红色元素需带发光效果增强可见度

---

## 二、素材获取状态（迭代区）

### 第 1 轮素材获取

| 序号  | 素材名称                  | 用途        | 获取方式             | 文件路径                                   | 质量评分 | 状态    | 说明                              |
| --- | --------------------- | --------- | ---------------- | -------------------------------------- | ---- | ----- | ------------------------------- |
| 1   | OpenClaw Logo (SVG)   | 封面主视觉、架构图 | material-fetcher | fig/素材/logo_openclaw_favicon.svg       | 90   | ✅ 已获取 | SVG 格式，64x64，官网 favicon，可缩放⭐推荐  |
| 2   | OpenClaw Logo (PNG)   | 备选 Logo   | material-fetcher | fig/素材/logo_openclaw_icon.png          | 75   | ✅ 已获取 | PNG 格式，32x32，官网 icon            |
| 3   | OpenClaw Logo (Apple) | 备选 Logo   | material-fetcher | fig/素材/logo_openclaw_apple.png         | 75   | ✅ 已获取 | PNG 格式，180x180，Apple touch icon |
| 4   | OpenClaw Logo (Org)   | 备选 Logo   | material-fetcher | fig/素材/logo_openclaw_org.png           | 75   | ✅ 已获取 | PNG 格式，400x400，GitHub 组织头像      |
| 5   | README 截图 1           | 架构图参考     | material-fetcher | fig/素材/readme_openclaw_openclaw_01.jpg | -    | ✅ 已获取 | GitHub README，架构示意图             |
| 6   | README 截图 2           | 架构图参考     | material-fetcher | fig/素材/readme_openclaw_openclaw_02.jpg | -    | ✅ 已获取 | GitHub README，功能展示              |
| 7   | README 截图 3           | 架构图参考     | material-fetcher | fig/素材/readme_openclaw_openclaw_03.jpg | -    | ✅ 已获取 | GitHub README，集成示例              |
| 8   | README 截图 4           | 架构图参考     | material-fetcher | fig/素材/readme_openclaw_openclaw_04.jpg | -    | ✅ 已获取 | GitHub README，配置示例              |
| 9   | README 截图 5           | 架构图参考     | material-fetcher | fig/素材/readme_openclaw_openclaw_05.jpg | -    | ✅ 已获取 | GitHub README，使用示例              |
| 10  | 应用界面截图                | 架构图参考     | 人工搜索             | fig/素材/screenshot.png                  | 85   | ✅ 已获取 | OpenClaw Gateway Dashboard 完整界面，含左侧导航和 Chat 区域 |
| 11  | ClawJacked 漏洞图        | 攻击路径图参考   | 人工搜索             | fig/素材/clawjacked_diagram.png          | 85   | ✅ 已获取 | GitHub Security Advisory (CVE-2026-25253)，含 CVSS 8.8 评分详情 |

---

### 补充素材清单（第 1 轮）

**视觉-planner 评估**：✅ 所有核心素材已获取完成。
- Logo 素材：SVG 格式质量分 90，PNG 备选 4 张
- 界面截图：OpenClaw Gateway Dashboard 完整界面（质量分 85）
- 漏洞参考：GitHub Security Advisory 官方页面（质量分 85）

**评估结论**：素材已足够，可以进入精修版规划。

| 序号  | 素材名称           | 用途             | 建议搜索关键词                                                             | 建议来源                              | 优先级 | 负责方 | 状态 |
| --- | -------------- | -------------- | ------------------------------------------------------------------- | --------------------------------- | --- | --- | ---- |
| 1   | 应用界面截图         | 架构图参考，展示真实 UI  | `OpenClaw UI screenshot`、`OpenClaw dashboard`                       | 官方文档、GitHub README                | P1  | 人工  | ✅ 已完成 |
| 2   | ClawJacked 漏洞图 | 攻击路径图参考，展示漏洞原理 | `ClawJacked vulnerability diagram`、`Oasis Security OpenClaw report` | Oasis Security 安全报告、TheHackerNews | P1  | 人工  | ✅ 已完成 |

**人工搜索指引**（已完成）：
1. **应用界面截图**：OpenClaw Gateway Dashboard 已保存至 `fig/素材/screenshot.png`
2. **ClawJacked 漏洞图**：GitHub Security Advisory (CVE-2026-25253) 已保存至 `fig/素材/clawjacked_diagram.png`

---

## 三、图片执行脚本（visual-planner 精修版）

**状态**：✅ 精修版规划完成，等待 visual-post-builder 执行

**版本**：v1.1 精修版
**完成时间**：2026-03-10
**规划 Agent**：visual-planner

### 图片结构总览

| id | 用途 | information_role | 获取方式 | 状态 |
|----|------|------------------|----------|------|
| 01 | 封面 | cover | hybrid-edit | ✅ 已规划 |
| 02 | 架构图解 | concept | hybrid-edit | ✅ 已规划 |
| 03 | 时间线 | timeline | ai-generate | ✅ 已规划 |
| 04 | 攻击路径 | flow | hybrid-edit | ✅ 已规划 |
| 05 | 风险对比表 | evidence | ai-generate | ✅ 已规划 |
| 06 | 防护清单 | checklist | ai-generate | ✅ 已规划 |
| 07 | 核心论点总结 | quote | ai-generate | ✅ 已规划 |

---

### 01_cover（封面）

**📋 需要提供的素材**：
| 素材 | 文件路径 | 融合方式 |
|------|----------|----------|
| OpenClaw Logo (SVG) | `fig/素材/logo_openclaw_favicon.svg` | 上传到 Discord 后作为图生图输入，prompt 详细描述 Logo 在画面中的位置和融合效果 |

> **使用方法**：
> 1. 将 `logo_openclaw_favicon.svg` 转为 PNG 后上传到 Discord
> 2. 复制图片链接
> 3. 使用下方「带参考图版」prompt，将链接填入 `[上传的 Logo 图片链接]`

---

**核心定义**：
- purpose: 建立「本地服务暴露于公网」的核心风险认知，用视觉叙事传达 ClawJacked 漏洞的本质
- theme_anchor: 「敞开的门」+「外部威胁」—— 本地代理正向互联网无条件敞开
- text_binding: 标题「OpenClaw 突然火了，但这些安全隐患你必须知道」
- visual_goal: 让读者第一眼感受到「你的电脑正向整个互联网敞开大门」的危险
- failure_mode:
  - 过度恐慌感（骷髅、黑客面具等陈词滥调）
  - 廉价 AI 发光效果（紫色/蓝色光晕滥用）
  - 通用素材感（与 OpenClaw 无关联的图库图）
  - Logo 质量过低导致锯齿
  - 只有抽象警示但没有具体风险意象

**执行策略**：
- source_route: hybrid-edit（AI 生成背景 + Logo 融合 + 文字叠加）
- builder_freedom:
  - 背景明暗/对比度微调
  - Logo 位置与大小优化
  - 文字阴影/描边参数调整
  - 红色警示元素的强度控制
- must_have:
  - SVG Logo（`logo_openclaw_favicon.svg`）置于视觉中心或黄金分割点
  - 深黑背景 (#050505 为主)
  - 高饱和暗红 (#FF3333) 作为警示强调色，需带发光效果
  - 主标题预留区域（中上部，高对比度）
  - 角标「AI 安全深度分析」位置（左上或右上）
  - 文字与背景对比度≥7:1
- must_avoid:
  - Logo 锯齿或模糊
  - 背景过于花哨干扰文字
  - 红色滥用导致视觉疲劳
  - 文字与背景对比度不足

**执行指令**：
- execution_instruction: |
  1. 使用 `logo_openclaw_favicon.svg` 作为主视觉元素（64x64 SVG 可无损放大）
  2. 生成「敞开的门户」背景：深黑底色 + 高饱和度红色辐射光束 + 外部攻击者剪影
  3. Logo 放置于门户中央阈值位置，成为「本地代理暴露」的视觉锚点
  4. Logo 周围添加强烈红色光晕，与外部网络空间形成对比
  5. 叠加主标题「OpenClaw 突然火了」+ 副标题「这些安全隐患你必须知道」
  6. 左上角添加角标「AI 安全深度分析」
  7. 输出前检查 Logo 边缘清晰度、文字对比度、红色饱和度

- prompt / keywords: |
  ## Midjourney v6 提示词（安全警示风格）

  ### 核心视觉概念

  **封面要讲的故事**：
  > 「你的本地代理服务，正向整个互联网敞开大门」

  **视觉隐喻**：
  - 一个发光的「门户/通道」从本地电脑延伸到外部网络
  - 外部有无数模糊的「攻击者剪影」正通过这个门户进入
  - OpenClaw Logo 位于门户中央，既是入口也是风险点
  - 高饱和度红色表示「危险通道」，与深色背景形成强烈对比

  ### 方式 A：带参考图版（推荐，需上传 Logo）

  **步骤**：
  1. 将 `logo_openclaw_favicon.svg` 转为 PNG 后上传到 Discord
  2. 复制图片链接
  3. 填入下方 prompt 中的 `[上传的 Logo 图片链接]`

  **风格说明**：
  - 核心意象：敞开的数字之门，本地服务暴露于公网
  - 视觉叙事：从门户中心向外辐射的危险信号
  - 设计感：简洁聚焦、高对比度、强视觉冲击

  ```
  /imagine prompt: [上传的 Logo 图片链接] cybersecurity breach concept art with the uploaded claw logo at center, a glowing portal or gateway opening from a computer into the vast internet darkness, countless shadowy attacker silhouettes approaching through the open gateway from outside, intense crimson red light radiating from the portal suggesting extreme danger, the claw logo positioned at the gateway threshold as both entrance and vulnerability point, high contrast deep black background with oversaturated red warning beams, dramatic perspective lines converging at center, sense of digital invasion and exposed local network, professional security report cover style, urgent cautionary atmosphere, no text, no watermark --ar 3:4 --stylize 300 --v 6
  ```

  **融合说明**：
  - 上传的 Logo 放置于画面中央「门户」的阈值位置
  - Logo 成为「本地代理暴露」的视觉锚点
  - 从门户向外辐射高饱和度红色光束，形成危险通道
  - 外部网络空间用深色剪影暗示潜在攻击者
  - 画面顶部和底部留白供标题文字叠加
  - 整体氛围传达「你的电脑正向互联网敞开」的风险感知

  ### 方式 B：纯背景版（无需上传，Logo 由 post-builder 后期叠加）

  ```
  /imagine prompt: cybersecurity breach concept art, a glowing portal or gateway opening from a computer into the vast internet darkness, countless shadowy attacker silhouettes approaching through the open gateway from outside, intense crimson red light radiating from the portal suggesting extreme danger, empty center space for logo overlay, high contrast deep black background with oversaturated red warning beams, dramatic perspective lines converging at center, sense of digital invasion and exposed local network, professional security report cover style, urgent cautionary atmosphere, no text, no watermark --ar 3:4 --stylize 300 --v 6
  ```

  **后期融合说明**：
  - AI 生成背景后，post-builder 将 Logo SVG 放置于「门户」中央阈值位置
  - Logo 成为「本地代理暴露」的视觉锚点
  - Logo 周围添加强烈红色光晕增强危险感
  - 确保 Logo 与背景明暗对比足够，红色饱和度高

  **关键词分解**：
  - 主体：glowing portal/gateway（发光门户/通道）
  - 威胁：shadowy attacker silhouettes approaching（逼近的攻击者剪影）
  - 风险意象：exposed local network, digital invasion（本地网络暴露、数字入侵）
  - 风格：cybersecurity breach concept art（网络安全漏洞概念艺术）
  - 色彩：deep black + **oversaturated crimson red**（深黑 + 过饱和深红）
  - 构图：perspective lines converging at center（透视线汇聚于中心）
  - 禁止：no text, no watermark, no generic claw imagery

- ratio: 3:4 (推荐 3000x4000 或 1242x1660)

---

### 02_architecture（架构图解）

**📋 需要提供的素材**：
| 素材 | 文件路径 | 融合方式 |
|------|----------|----------|
| OpenClaw Dashboard 截图 | `fig/素材/screenshot.png` | 上传到 Discord 后作为图生图输入，prompt 详细描述界面布局和配色风格 |

> **使用方法**：
> 1. 将 `screenshot.png` 上传到 Discord
> 2. 复制图片链接
> 3. 使用下方「带参考图版」prompt，将链接填入 `[上传的截图链接]`

---

**核心定义**：
- purpose: 直观展示 OpenClaw「Gateway + Node」架构，揭示「沙箱默认关闭 = 宿主机直接执行」的风险本质
- theme_anchor: 「连接」+「权限边界」—— Gateway 作为中枢连接各方，但沙箱缺失导致风险直连宿主机
- text_binding: 正文中「OpenClaw 架构解析」与「沙箱默认关闭」相关段落
- visual_goal: 让读者理解「这个架构很强大，但权限边界模糊是隐患」
- failure_mode:
  - 过度复杂的技术图（过多节点、连线）
  - 与 OpenClaw 实际架构不符
  - 颜色混乱导致信息层级不清
  - 文字过小无法阅读

**执行策略**：
- source_route: hybrid-edit（AI 生成背景 + 架构图绘制 + 文字叠加）
- builder_freedom:
  - 架构图节点位置微调
  - 连线粗细/颜色优化
  - 背景渐变强度
  - 文字大小与间距
- must_have:
  - Gateway 模块（标注端口 :18789）
  - 终端命令执行、文件系统读写、浏览器控制等能力模块
  - 渠道集成模块（WhatsApp/Telegram/Slack）
  - 底部警示条「⚠️ 沙箱默认关闭 = 宿主机直接执行」
  - 参考 `screenshot.png` 中的界面风格（左侧导航 + 深色主题）
  - 深黑背景 + 科技蓝/白色文字
- must_avoid:
  - 架构图过于拥挤
  - 颜色超过 3 种主色
  - 警示信息不够醒目
  - 连线交叉混乱

**执行指令**：
- execution_instruction: |
  1. 参考 `screenshot.png` 中的 OpenClaw 界面风格（左侧导航 + 深色主题）
  2. 绘制架构图：
     - 顶部：Gateway（本地服务，端口:18789）
     - 右侧：终端命令执行、文件系统读写、浏览器控制、摄像头/麦克风、剪贴板/定位
     - 底部：渠道集成（WhatsApp、Telegram、Slack 等）
  3. 使用科技蓝色表示正常连接，暗红色标注风险点
  4. 底部添加醒目警示条「⚠️ 沙箱默认关闭 = 宿主机直接执行」
  5. 确保文字清晰可读，层级分明

- prompt / keywords: |
  ## Midjourney v6 提示词（可爱科技设计风）

  ### 方式 A：带参考图版（推荐，需上传截图）

  **步骤**：
  1. 将 `screenshot.png` 上传到 Discord
  2. 复制图片链接
  3. 填入下方 prompt 中的 `[上传的截图链接]`

  **风格说明**：
  - 可爱感：圆润的模块边框、友好的界面气质
  - 科技感：渐变光影、网络节点、未来感
  - 设计感：简洁布局、充足留白、清晰层级

  ```
  /imagine prompt: [上传的截图链接] cute tech diagram background inspired by the uploaded dashboard screenshot, friendly software interface aesthetic with left sidebar navigation layout, deep black to dark blue gradient background, subtle network node pattern in corners suggesting connectivity, clean central area for architecture diagram overlay, minimalist cyber security style with approachable feel, soft rounded corners on UI elements, faint grid lines for alignment, no text, no watermark --ar 16:9 --stylize 100 --v 6
  ```

  **融合说明**：
  - 上传的截图作为风格参考，AI 会提取其深色界面美学和左侧导航布局
  - 背景生成深蓝渐变，角落点缀网络节点图案
  - 模块边框圆润柔和，避免尖锐棱角
  - 中央留白区域用于后期绘制架构图

  ### 方式 B：纯背景版（无需上传，架构图由 post-builder 后期绘制）

  ```
  /imagine prompt: cute tech diagram background, friendly software interface aesthetic with left sidebar navigation hint, deep black to dark blue gradient, subtle network node pattern in corners, clean central area for architecture diagram, minimalist cyber security style with approachable feel, soft rounded corners, faint grid lines, no text, no watermark --ar 16:9 --stylize 100 --v 6
  ```

  **后期融合说明**：
  - AI 生成背景后，post-builder 参考 `screenshot.png` 的界面风格绘制架构图
  - 提取左侧导航栏布局、深色主题配色、科技蓝强调色
  - 中央留白区域用于绘制架构图和叠加文字
  - 模块卡片使用圆角设计，增强亲和力

- ratio: 16:9 (推荐 1920x1080 或 3840x2160)

---

### 03_timeline（安全事件时间线）

**核心定义**：
- purpose: 梳理 2026.01-2026.03 期间 OpenClaw 相关安全事件，建立「风险持续暴露」的时间认知
- theme_anchor: 「时间流逝」+「风险累积」—— 每个时间节点都是风险拼图的一块
- text_binding: 正文中「安全事件时间线」相关段落
- visual_goal: 让读者感受到「这不是单一事件，而是持续暴露的风险链条」
- failure_mode:
  - 时间线过于拥挤，文字无法阅读
  - 节点视觉权重平均，无重点
  - 与正文描述的时间/事件不一致
  - 通用时间线模板感（缺乏安全主题特征）

**执行策略**：
- source_route: ai-generate
- builder_freedom:
  - 时间线走向（横向/纵向）可根据画面调整
  - 节点颜色深浅微调
  - 背景纹理强度
  - 文字大小与行距
- must_have:
  - 4 个关键节点：2026.01 RCE 漏洞修复、2026.02.09 4.3 万实例暴露、2026.02.19 ClawHub 恶意技能、2026.02.25 ClawJacked 漏洞披露
  - 每个节点标注事件名称 + 简要说明
  - 暗红 (#DC2626) 标注高风险节点
  - 深黑背景 + 白色文字
  - 时间轴线条清晰可见
- must_avoid:
  - 节点过多导致拥挤
  - 文字与背景对比度不足
  - 时间顺序错误
  - 轴线条被背景淹没

**执行指令**：
- execution_instruction: |
  1. 生成深色科技背景：深黑渐变 + 微妙时间流逝感（如淡化日历/时钟元素）
  2. 绘制横向时间轴，左起 2026.01，右至 2026.02.25
  3. 标注 4 个关键节点：
     - 2026.01: RCE 漏洞修复 (CVE-2026-25253 等)
     - 2026.02.09: 4.3 万实例暴露公网，1.5 万存在 RCE 漏洞
     - 2026.02.19: ClawHub 发现 1184 个恶意技能，含 curl | bash 窃密脚本
     - 2026.02.25: ClawJacked 漏洞披露，任意网站可暴力破解本地代理
  4. 使用暗红标注 ClawJacked 节点（当前最新、最严重）
  5. 确保文字清晰，时间轴线条可见

- prompt / keywords: |
  **Midjourney v6 (背景底图)**:
  ```
  /imagine prompt: horizontal timeline background, cyber security theme, deep black to dark charcoal gradient, subtle red alert glow at right edge suggesting escalating threat, faint digital clock or calendar pattern in background, clean horizontal path for timeline, professional infographic style, no text, no watermark --ar 21:9 --stylize 150 --v 6
  ```

  **时间线节点关键词**:
  - 节点形状：圆形/菱形，暗红填充 + 白色描边
  - 连接线：白色/浅灰实线，2-3px 粗细
  - 文字：白色无衬线字体，标题加粗，说明文字常规
  - 背景：深黑渐变，右侧暗红光晕增强

- ratio: 21:9 (推荐 4200x1800 横向长图)

---

### 04_attack_flow（ClawJacked 攻击路径）

**📋 需要提供的素材**：
| 素材 | 文件路径 | 融合方式 |
|------|----------|----------|
| ClawJacked 漏洞图 | `fig/素材/clawjacked_diagram.png` | 上传到 Discord 后作为图生图输入，prompt 详细描述 GitHub Security Advisory 页面风格和 CVSS 徽章元素 |

> **使用方法**：
> 1. 将 `clawjacked_diagram.png` 上传到 Discord
> 2. 复制图片链接
> 3. 使用下方「带参考图版」prompt，将链接填入 `[上传的漏洞图链接]`

---

**核心定义**：
- purpose: 可视化 ClawJacked 漏洞 (CVE-2026-25253) 的完整攻击链路，揭示「任意网站可接管本地代理」的风险机制
- theme_anchor: 「入侵路径」+「权限失守」—— 从浏览网页到完全接管的逐步沦陷
- text_binding: 正文中「ClawJacked 攻击路径分析」相关段落
- visual_goal: 让读者理解「只是浏览网页就可能被接管本地代理」的严重性
- failure_mode:
  - 流程图过于复杂，无法一眼理解
  - 与 GitHub Security Advisory 描述不一致
  - 过度使用恐吓性图标（骷髅、红色警报等）
  - 箭头走向混乱，阅读顺序不清

**执行策略**：
- source_route: hybrid-edit（AI 生成背景 + 流程图绘制 + 文字叠加）
- builder_freedom:
  - 流程图节点形状选择（矩形/圆角矩形）
  - 箭头样式（实线/虚线/渐变）
  - 背景纹理强度
  - 每步骤说明文字长度
- must_have:
  - 6 步完整攻击链：用户浏览网页 → 误入钓鱼网站 → JS 连接 localhost:18789 → 暴力破解密码 → 注册为受信设备 → 完全接管代理
  - 参考 `clawjacked_diagram.png` 中的 GitHub Security Advisory 官方描述和 CVSS 8.8 评分
  - 暗红色标注关键风险步骤
  - 垂直流程图布局（符合阅读习惯）
  - 每步骤配简洁说明文字
- must_avoid:
  - 箭头交叉或回环
  - 步骤说明文字过长
  - 颜色超过 3 种
  - 与 CVE 描述矛盾

**执行指令**：
- execution_instruction: |
  1. 参考 `clawjacked_diagram.png` 中的 GitHub Security Advisory 官方描述
  2. 生成深色背景：深黑到暗红渐变，暗示「逐步沦陷」
  3. 绘制垂直流程图（6 步）：
     - Step 1: 用户浏览网页
     - Step 2: 误入钓鱼网站
     - Step 3: 网站 JS 连接 localhost:18789
     - Step 4: 暴力破解密码（本地不限速）
     - Step 5: 注册为受信设备
     - Step 6: 完全接管代理 → 执行任意命令/读取文件/访问日志
  4. Step 4-6 使用暗红边框/背景强调风险升级
  5. 右侧标注 CVSS 8.8（高危）评分

- prompt / keywords: |
  ## Midjourney v6 提示词（可爱科技设计风）

  ### 方式 A：带参考图版（推荐，需上传漏洞图）

  **步骤**：
  1. 将 `clawjacked_diagram.png` 上传到 Discord
  2. 复制图片链接
  3. 填入下方 prompt 中的 `[上传的漏洞图链接]`

  **风格说明**：
  - 可爱感：圆润的流程图节点、友好的视觉语言
  - 科技感：渐变光影、安全主题元素、未来感
  - 设计感：简洁垂直布局、充足留白、清晰层级

  ```
  /imagine prompt: [上传的漏洞图链接] cute tech flowchart background inspired by GitHub Security Advisory page style, friendly visual language with rounded flowchart nodes, the uploaded vulnerability diagram shows CVSS 8.8 score badge and professional security report layout, deep black at top gradient to warm dark red at bottom suggesting escalating danger, subtle warning triangle patterns faded in background, clean vertical path for flow arrows, minimalist tech infographic style with approachable feel, soft rounded corners on elements, no text, no watermark --ar 3:4 --stylize 150 --v 6
  ```

  **融合说明**：
  - 上传的漏洞图作为风格参考，AI 会提取 GitHub Security Advisory 页面的专业安全报告风格
  - 背景右上角可有微妙的 CVSS 评分徽章图案暗示
  - 整体色调为深黑到暖暗红渐变，暗示「逐步沦陷」的风险升级
  - 流程图节点使用圆角设计，增强亲和力

  ### 方式 B：纯背景版（无需上传，流程图由 post-builder 后期绘制）

  ```
  /imagine prompt: cute tech flowchart background, friendly visual language with rounded flowchart nodes, cyber security breach theme, deep black at top gradient to warm dark red at bottom, subtle warning triangle patterns, clean vertical path for flow arrows, minimalist tech infographic style with approachable feel, GitHub Security Advisory page aesthetic with CVSS score badge visible in corner, soft rounded corners, no text, no watermark --ar 3:4 --stylize 150 --v 6
  ```

  **后期融合说明**：
  - AI 生成背景后，post-builder 参考 `clawjacked_diagram.png` 的 GitHub Security Advisory 页面风格绘制流程图
  - 背景右下角可有微妙的 CVSS 8.8 徽章图案暗示
  - 整体色调与截图一致：深黑到暗红渐变，暗示「逐步沦陷」的风险升级
  - 右侧留白区域用于标注 CVSS 评分
  - 流程图节点使用圆角设计，增强亲和力

- ratio: 3:4 (推荐 3000x4000 或 1242x1660)

---

### 05_risk_matrix（风险对比表）

**核心定义**：
- purpose: 对比普通用户、开发者、企业三类人群在各类风险中的暴露程度，帮助读者对号入座
- theme_anchor: 「风险差异」+「身份认知」—— 不同角色面临不同等级的风险
- text_binding: 正文中「谁的风险最大」相关段落
- visual_goal: 让读者快速找到自己的身份定位并感知风险等级
- failure_mode:
  - 表格过于复杂，星级/颜色过多
  - 风险等级标识不清晰
  - 文字过小无法阅读
  - 与正文描述的风险等级不一致

**执行策略**：
- source_route: ai-generate
- builder_freedom:
  - 表格行数/列数微调
  - 星级颜色（红/橙/黄）
  - 背景纹理强度
  - 文字大小与行距
- must_have:
  - 5 类风险：核心平台漏洞、供应链风险、分发伪装、部署配置、权限滥用
  - 3 类人群：普通用户、开发者、企业
  - 风险等级用圆点表示（●实心 + ○空心组合）
  - 深黑背景 (#050505) + 白色文字 + 科技蓝表头
  - 高危圆点：#FF4444 带发光效果
  - 中危圆点：#FFC040 带发光效果
  - 低危圆点：#6B7280 无发光
  - 表格线条清晰可见，行间对比度≥4:1
- must_avoid:
  - 颜色过多（超过 4 种）
  - 星级标识混乱
  - 表格线条与背景融为一体
  - 文字与单元格不对齐

**执行指令**：
- execution_instruction: |
  1. 生成深色表格背景：深黑底 (#050505) + 微妙网格线
  2. 绘制表格：
     - 表头：风险类型 | 普通用户 | 开发者 | 企业
     - 5 行风险项，每项用 8 个圆点表示风险等级（●实心 + ○空心）
  3. 风险等级说明：
     - ●●●●●●●●○ 高危（#FF4444 带发光）
     - ●●●●●●○○ 中高危（#FFC040 带发光）
     - ●●●●○○○○ 中低危（#6B7280）
  4. 表头使用科技蓝 (#3B82F6) 背景
  5. 确保文字清晰，圆点对齐，发光效果明显

- prompt / keywords: |
  **Midjourney v6 (背景底图)**:
  ```
  /imagine prompt: data table background, dark professional tech style, subtle grid lines visible in deep black background, clean cells for data entry, cyber security dashboard aesthetic, faint blue accent in header area, minimalist corporate tech, no text, no watermark --ar 16:10 --stylize 100 --v 6
  ```

  **表格元素关键词**:
  - 表头：科技蓝背景 + 白色加粗文字
  - 行：深黑卡片 + 浅灰边框，隔行深色区分
  - 星级：★ 符号，暗红/橙/黄/灰区分等级
  - 线条：浅灰 #4B5563，1-2px 粗细

- ratio: 16:10 (推荐 3200x2000)

---

### 06_checklist（防护清单）

**核心定义**：
- purpose: 提供可立即执行的防护措施清单，降低读者焦虑感并转化为行动
- theme_anchor: 「可操作性」+ 「防护意识」—— 从被动担忧到主动防护
- text_binding: 正文中「如何安全使用 OpenClaw」相关段落
- visual_goal: 让读者感受到「有具体方法可以保护自己」的安心感
- failure_mode:
  - 清单条目过多导致压力
  - 表述过于技术化难以理解
  - 缺少明确的行动指引
  - 通用清单模板感（缺乏安全主题特征）

**执行策略**：
- source_route: ai-generate
- builder_freedom:
  - 清单条目数量（建议 8-10 条）
  - 复选框样式（方形/圆形/盾牌形）
  - 背景纹理强度
  - 文字大小与行距
- must_have:
  - 10 条核心防护建议（只从官网下载、更新最新版本、只监听 127.0.0.1、不暴露公网、虚拟机/容器运行、不以管理员身份运行、仅与可信联系人配对、群聊启用@提及、只安装可信技能、不存储敏感凭证）
  - 复选框符号（□ 或 ☐）
  - 深黑背景 + 白色文字
  - 科技蓝 (#2563EB) 强调 actionable 项目
  - 标题「防护清单（正在使用的人必看）」
- must_avoid:
  - 条目文字过长
  - 复选框与文字不对齐
  - 颜色过多干扰阅读
  - 缺少标题

**执行指令**：
- execution_instruction: |
  1. 生成深色清单背景：深黑底 + 微妙复选框纹理
  2. 绘制清单（10 条）：
     - □ 只从官网/GitHub 官方下载
     - □ 更新至最新版本 (2026.2.25+)
     - □ 只监听 127.0.0.1:18789
     - □ 不暴露公网
     - □ 虚拟机/容器中运行
     - □ 不以管理员身份运行
     - □ 仅与可信联系人配对
     - □ 群聊启用@提及策略
     - □ 只安装可信开发者技能
     - □ 不存储敏感凭证在配置中
  3. 标题「防护清单（正在使用的人必看）」置于顶部
  4. 复选框使用浅灰/白色，可 hover 状态暗示可交互
  5. 确保文字清晰，行距适中

- prompt / keywords: |
  **Midjourney v6 (背景底图)**:
  ```
  /imagine prompt: checklist background, dark professional tech aesthetic, subtle checkbox outlines on left side forming a column, clean list area with faint horizontal guide lines, cyber security briefing style, deep black background with faint gray lines, minimalist design, no text, no watermark --ar 3:4 --stylize 100 --v 6
  ```

  **清单元素关键词**:
  - 复选框：浅灰 #9CA3AF 方形，16-20px 尺寸
  - 文字：白色无衬线字体，14-16px 等效
  - 标题：科技蓝背景 + 白色加粗文字
  - 背景：深黑 #0D0D0D + 浅灰水平分隔线

- ratio: 3:4 (推荐 3000x4000 或 1242x1660)

---

### 07_summary_card（核心论点总结）

**核心定义**：
- purpose: 凝练全文核心论点，形成可传播、可引用的金句卡片
- theme_anchor: 「功能即风险边界」—— 全文核心论点的视觉凝练
- text_binding: 正文结尾「核心论点」与结语部分
- visual_goal: 让读者愿意收藏/转发这张卡片，形成二次传播
- failure_mode:
  - 文字过多导致卡片拥挤
  - 缺乏视觉焦点和金句突出
  - 与全文调性不一致（过于轻松或过于严肃）
  - 通用金句模板感（缺乏 OpenClaw 特征）

**执行策略**：
- source_route: ai-generate
- builder_freedom:
  - 卡片背景纹理（渐变/网格/抽象图案）
  - Logo 位置与大小
  - 文字层级（标题/正文/金句）
  - 留白比例
- must_have:
  - 6 条核心论点（不是普通聊天 AI、官方信任模型仅限个人使用、ClawHub 供应链风险、ClawJacked 证明过度信任本地是隐患、默认配置是隐患、防护基石是最小权限和隔离）
  - 金句「功能即风险边界，越像操作系统的工具越需要专业部署」
  - OpenClaw Logo（小尺寸置于角落）
  - 深黑背景 + 白色文字
  - 暗红/科技蓝强调金句
- must_avoid:
  - 文字堆砌无留白
  - 金句不够突出
  - Logo 过大抢镜
  - 颜色过多

**执行指令**：
- execution_instruction: |
  1. 生成深色卡片背景：深黑渐变 + 微妙纹理
  2. 布局规划：
     - 顶部：标题「OpenClaw 安全性分析 - 核心论点」
     - 中部：6 条核心论点（编号列表）
     - 底部：金句「功能即风险边界，越像操作系统的工具越需要专业部署」（放大 + 强调色）
  3. Logo 使用小尺寸 SVG 置于右上角或底部中央
  4. 金句使用暗红 (#DC2626) 或科技蓝 (#2563EB) 强调
  5. 确保文字层级清晰，留白充足

- prompt / keywords: |
  **Midjourney v6 (背景底图)**:
  ```
  /imagine prompt: quote card background, dark minimalist tech style, subtle gradient from deep black to dark charcoal, clean centered area for text, faint abstract claw silhouette in corner, professional presentation aesthetic, cyber security report style, no text, no watermark --ar 3:4 --stylize 100 --v 6
  ```

  **卡片元素关键词**:
  - 标题：白色加粗，20-24px 等效
  - 列表：白色常规，14-16px 等效，行距 1.5
  - 金句：暗红/科技蓝 + 加粗，18-20px 等效，上下留白
  - Logo：小尺寸 SVG，置于右上角或底部中央
  - 背景：深黑 #0D0D0D 到暗灰 #1F1F1F 渐变

- ratio: 3:4 (推荐 3000x4000 或 1242x1660)

---

## 四、执行日志（post-builder 填写）

**状态**：⚪ 等待 visual-post-builder 执行

### 执行前检查清单

- [ ] 确认所有素材文件存在于 `fig/素材/` 目录
- [ ] 确认 Logo SVG 文件可无损放大
- [ ] 确认 AI 绘图工具已配置（Midjourney / Stable Diffusion）
- [ ] 确认输出目录 `fig/定稿图/` 已创建

### 执行日志模板

### 01_cover
- 原始素材：
- 执行方式：
- 做了哪些优化：
- 为什么选这一版：
- 输出文件：
- 尺寸：

---

## 五、审核意见（visual-reviewer 填写）

**审核时间**：2026-03-11T12:00:00
**审核员**：visual-reviewer

### 优化记录（2026-03-11 更新）

**问题反馈**：
1. 封面缺少 OpenClaw Logo
2. 画面色彩饱和度太低，太暗
3. 图 5 风险矩阵图标与背景几乎融合，看不清

**优化方案**：
1. **封面 Logo**：嵌入 SVG Logo 代码，添加红色发光效果
2. **色彩饱和度**：
   - 背景从 #0D0D0D 改为 #050505（更深）
   - 红色从 #DC2626 改为 #FF3333（更高饱和）
   - 蓝色从 #2563EB 改为 #3B82F6（更亮）
   - 次要文字从 #9CA3AF 改为 #E5E5E5（更亮）
3. **风险矩阵**：
   - 改用 CSS 圆点 (`.dot`) 替代文本符号 (●/○)
   - 高危圆点：#FF4444 带发光效果 (`box-shadow`)
   - 中危圆点：#FFC040 带发光效果
   - 空心圆点：透明背景 + 灰色边框

**执行日志**：
- 已更新 `generate_xhs_images.py`
- 已重新生成 7 张图片
- 已更新本章色彩规范

---

### 单图审核

| 图号 | 用途 | 主题贴合度 | 视觉质量 | 平台适配度 | 素材规范 | 审核结论 | 修改意见 |
|------|------|------------|----------|------------|----------|----------|----------|
| 01 | 封面 | ★★★★★ | ★★★★★ | ★★★★★ | ✅ | ✅ 通过 | Logo 已添加，发光效果良好 |
| 02 | 架构图解 | ★★★★★ | ★★★★★ | ★★★★★ | ✅ | ✅ 通过 | - |
| 03 | 时间线 | ★★★★★ | ★★★★★ | ★★★★★ | ✅ | ✅ 通过 | - |
| 04 | 攻击路径 | ★★★★★ | ★★★★★ | ★★★★★ | ✅ | ✅ 通过 | - |
| 05 | 风险对比表 | ★★★★★ | ★★★★★ | ★★★★★ | ✅ | ✅ 通过 | 圆点对比度已修复 |
| 06 | 防护清单 | ★★★★★ | ★★★★★ | ★★★★★ | ✅ | ✅ 通过 | - |
| 07 | 核心论点总结 | ★★★★★ | ★★★★★ | ★★★★★ | ✅ | ✅ 通过 | - |

### 整体评估

- **风格统一性**：★★★★★ - 整套图采用统一的深黑背景 (#050505)、科技蓝 (#3B82F6)、高饱和红 (#FF3333) 配色，风格高度一致
- **叙事连贯性**：★★★★★ - 从封面抓眼球 → 架构解析 → 时间线 → 攻击路径 → 风险矩阵 → 防护清单 → 核心论点，逻辑清晰
- **平台适配度**：★★★★★ - 3:4 比例符合小红书规范，内容完整无截断
- **审美完成度**：★★★★★ - 无廉价 AI 感，暗黑科技风统一，信息层级清晰，发光效果增强可见度

### 审核结论

- [x] ✅ 通过定稿
- [ ] 🔧 需要修改（见上方意见）
- [ ] ❌ 驳回重做（需重新规划）

### 是否可以定稿

**结论**：是

**理由**：
1. **封面图完整**：OpenClaw Logo 已嵌入，带红色发光效果，标题清晰显示
2. **无截断问题**：所有 7 张图片内容完整，无底部裁切
3. **视觉统一**：深黑背景 (#050505)、高饱和红 (#FF3333)、科技蓝 (#3B82F6) 贯穿整套图
4. **信息清晰**：风险矩阵圆点符号对比度良好（带发光效果），防护清单 10 条完整显示，核心论点 6 条 + 金句完整
5. **色彩饱和度提升**：所有强调色饱和度提高，文字对比度增强

---

### 发布包整理

**定稿图路径**：`02_内容项目/审稿中/OpenClaw 安全性分析/fig/output/`

| 文件名 | 用途 | 尺寸 |
|--------|------|------|
| 01_cover.png | 封面 | 1080x1920 |
| 02_architecture.png | 架构图解 | 1080x1920 |
| 03_timeline.png | 时间线 | 1080x1920 |
| 04_attack_flow.png | 攻击路径 | 1080x1920 |
| 05_risk_matrix.png | 风险矩阵 | 1080x1920 |
| 06_checklist.png | 防护清单 | 1080x1920 |
| 07_summary.png | 核心论点 | 1080x1920 |

**小红书适配稿**：`02_内容项目/审稿中/OpenClaw 安全性分析/OpenClaw 安全性分析_小红书适配稿.md`

**标题候选**：10 个（见适配稿）
**封面文案**：3 组（见适配稿）
**标签建议**：#AI 安全 #OpenClaw #网络安全 #漏洞分析 #AI 代理 #数据安全 #技术科普
**评论区引导语**：3 条（见适配稿）

---

## 六、AI 绘图提示词汇总（外部生图使用）

**状态**：✅ 已整合到各图执行脚本中，此处为快速索引

> 说明：以下提示词与「三、图片执行脚本」中各图的 prompt 字段互为补充。实际使用时，请以各图执行脚本中的 prompt 为准。

### 快速索引

| 图号 | 用途 | 获取方式 | Prompt 位置 |
|------|------|----------|-------------|
| 01 | 封面 | hybrid-edit | 见 01_cover 执行脚本 |
| 02 | 架构图解 | hybrid-edit | 见 02_architecture 执行脚本 |
| 03 | 时间线 | ai-generate | 见 03_timeline 执行脚本 |
| 04 | 攻击路径 | hybrid-edit | 见 04_attack_flow 执行脚本 |
| 05 | 风险对比表 | ai-generate | 见 05_risk_matrix 执行脚本 |
| 06 | 防护清单 | ai-generate | 见 06_checklist 执行脚本 |
| 07 | 核心论点总结 | ai-generate | 见 07_summary_card 执行脚本 |

### 统一参数建议

| 参数 | Midjourney | Stable Diffusion |
|------|------------|------------------|
| 比例 | 按各图要求 `--ar` | 按各图要求 `--ar` |
| 风格化 | `--stylize 100-250` | CFG Scale: 7 |
| 版本 | `--v 6` | 推荐 SDXL 或 MJ v6 模型 |
| 采样步数 | - | 30-50 steps |

### 生图后处理

1. **文字叠加**：使用 post-builder 或 Canva/PS 在背景图上叠加中文文字
2. **统一色调**：确保所有图片色调一致（深黑 #0D0D0D + 暗红 #DC2626 + 科技蓝 #2563EB）
3. **文字规范**：使用无衬线字体（思源黑体/苹方），标题加粗
4. **留白检查**：确保文字区域有足够对比度和留白
5. **Logo 整合**：封面和总结卡需整合 SVG Logo（`logo_openclaw_favicon.svg`）

---

## 附录：视觉规划历史版本

### v1.0（初版）
- 创建时间：2026-03-10
- 内容：7 张信息图规划 + 素材需求清单

### v1.1（精修版）
- 创建时间：2026-03-10
- 内容：基于已获取素材的详细执行方案，包含 7 张图的完整执行脚本和 AI 绘图提示词
- 规划 Agent：visual-planner

---

## 视觉内容清单（初版规划保留）

| 序号  | 用途     | 内容描述                        | 类型   | 优先级 |
| --- | ------ | --------------------------- | ---- | --- |
| 01  | 封面     | OpenClaw Logo + 安全警示视觉 + 标题 | 合成图  | P0  |
| 02  | 架构图解   | Gateway + Node 架构示意图        | 信息图  | P0  |
| 03  | 时间线    | 2026.01-2026.03 安全事件时间线     | 信息图  | P0  |
| 04  | 攻击路径   | ClawJacked 漏洞攻击流程           | 流程图  | P1  |
| 05  | 风险对比表  | 普通用户/开发者/企业风险等级             | 表格图  | P1  |
| 06  | 防护清单   | 安装部署/权限/凭证等防护建议             | 清单图  | P1  |
| 07  | 核心论点总结 | 6 条核心论点卡片                   | 文字卡片 | P2  |

---

## 逐图详细规划

### 图 1：封面

**内容要素**：
- OpenClaw 官方 Logo（红色爪形/钳子概念）
- 主标题：OpenClaw 突然火了
- 副标题：这些安全隐患你必须知道
- 角标：AI 安全深度分析
- 视觉基调：暗黑色 + 警示红

**制作方式**：
- 从 OpenClaw GitHub 仓库获取官方 Logo
- 深色背景 + 红色强调色
- 标题文字居中排版

**参考尺寸**：1242x1660 (3:4)

---

### 图 2：架构图解

**内容要素**：
```
┌─────────────────────────────────────────────────────┐
│                  OpenClaw 架构                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│   ┌──────────────┐         ┌──────────────────┐    │
│   │   Gateway    │◄───────►│   终端命令执行    │    │
│   │  (本地服务)   │         │   文件系统读写    │    │
│   │  :18789      │         │   浏览器控制      │    │
│   └──────┬───────┘         │   摄像头/麦克风   │    │
│          │                 │   剪贴板/定位     │    │
│          ▼                 └──────────────────┘    │
│   ┌──────────────┐                                 │
│   │  渠道集成     │                                 │
│   │ WhatsApp     │                                 │
│   │ Telegram     │                                 │
│   │ Slack 等     │                                 │
│   └──────────────┘                                 │
│                                                     │
│   ⚠️ 沙箱默认关闭 = 宿主机直接执行                   │
└─────────────────────────────────────────────────────┘
```

**制作方式**：信息图 / 架构图
**风格**：简洁技术风，深色背景 + 白色文字 + 蓝色/红色强调

---

### 图 3：安全事件时间线

**内容要素**：
```
2026.01        2026.02.09        2026.02.19       2026.02.25
  │                │                 │                │
  ▼                ▼                 ▼                ▼
┌──────────┐  ┌──────────┐   ┌──────────────┐  ┌────────────┐
│ RCE 漏洞  │  │ 4.3 万实例 │   │ ClawHub 发现  │  │ ClawJacked │
│ 修复     │  │ 暴露公网  │   │ 1184 恶意技能 │  │ 漏洞披露   │
└──────────┘  └──────────┘   └──────────────┘  └────────────┘
  CVE-2026-     1.5 万存在       窃密技能包        任意网站可
  25253 等       RCE 漏洞         含 curl | bash    暴力破解本地
```

**制作方式**：横向时间线信息图
**风格**：深色背景 + 红色警示节点

---

### 图 4：ClawJacked 攻击路径

**内容要素**：
```
用户浏览网页
     │
     ▼
误入钓鱼网站
     │
     ▼
网站 JS 连接 localhost:18789
     │
     ▼
暴力破解密码 (本地不限速)
     │
     ▼
注册为受信设备
     │
     ▼
完全接管代理 → 执行任意命令/读取文件/访问日志
```

**制作方式**：垂直流程图
**风格**：箭头流程 + 警示图标

---

### 图 5：风险对比表

**内容要素**：
| 风险类型 | 普通用户 | 开发者 | 企业 |
|----------|----------|--------|------|
| 核心平台漏洞 | ★★★☆ | ★★★☆ | ★★★★ |
| 供应链风险 | ★★☆☆ | ★★★★ | ★★★☆ |
| 分发伪装 | ★★★★ | ★★★☆ | ★★★☆ |
| 部署配置 | ★★☆☆ | ★★★☆ | ★★★★ |
| 权限滥用 | ★★★☆ | ★★★☆ | ★★★★ |

**制作方式**：表格信息图
**风格**：清晰可读，星级用★表示

---

### 图 6：防护清单

**内容要素**：
```
┌─────────────────────────────────────────┐
│  防护清单（正在使用的人必看）            │
├─────────────────────────────────────────┤
│  □ 只从官网/GitHub 官方下载              │
│  □ 更新至最新版本 (2026.2.25+)          │
│  □ 只监听 127.0.0.1:18789               │
│  □ 不暴露公网                           │
│  □ 虚拟机/容器中运行                     │
│  □ 不以管理员身份运行                    │
│  □ 仅与可信联系人配对                    │
│  □ 群聊启用@提及策略                     │
│  □ 只安装可信开发者技能                  │
│  □ 不存储敏感凭证在配置中                │
└─────────────────────────────────────────┘
```

**制作方式**：清单式信息图
**风格**：checklist 风格，增强可操作性感知

---

### 图 7：核心论点总结

**内容要素**：
```
OpenClaw 安全性分析 - 核心论点

1. 不是普通聊天 AI，是"操作系统级"代理
2. 官方信任模型仅限个人使用
3. ClawHub 供应链存在严重后门风险
4. ClawJacked 证明过度信任本地是隐患
5. 默认配置是安全隐患（上万实例暴露）
6. 防护基石是最小权限和隔离

功能即风险边界
越像操作系统的工具，越需要专业部署
```

**制作方式**：文字卡片
**风格**：简洁深色背景 + 白色文字

---

## 视觉风格规范

| 要素 | 规范 |
|------|------|
| **主色调** | 深黑 (#0D0D0D)、暗红 (#DC2626)、科技蓝 (#2563EB) |
| **辅助色** | 灰色 (#6B7280)、白色 (#FFFFFF) |
| **风格** | 暗黑科技风、信息图优先、简洁现代 |
| **字体** | 无衬线字体（思源黑体/苹方），标题加粗 |
| **情绪** | 警示、审慎、专业，避免过度恐慌或通用素材感 |

---

## 制作优先级

**第一阶段（P0 - 必须）**：
1. 封面图
2. 架构图解
3. 时间线

**第二阶段（P1 - 重要）**：
4. 攻击路径流程图
5. 风险对比表
6. 防护清单

**第三阶段（P2 - 可选）**：
7. 核心论点总结卡片

---

## 执行建议

- 信息图优先使用简洁排版 + 文字，不依赖外部素材
- OpenClaw Logo 使用 `material-fetcher` 技能从 GitHub 获取
- 所有图表保持统一的深色主题风格

---

## 执行指南

### 步骤 1：素材获取状态

**已获取素材**（使用 material-fetcher）：
- ✅ OpenClaw Logo: `fig/素材/logo_openclaw_org.png`（GitHub 组织头像）
- ✅ README 截图 5 张：`fig/素材/readme_openclaw_openclaw_*.jpg`

**需要人工搜索并下载的素材**：

| 序号 | 素材名称 | 用途 | 建议来源 | 保存路径 | 优先级 |
|------|----------|------|----------|----------|--------|
| 1 | **OpenClaw 官方 Logo（SVG 优先）** | 封面图主视觉 | `https://openclaw.ai` 官网 Brand/Press 页 | `fig/素材/logo_openclaw.svg` | P0 |
| 2 | **OpenClaw 应用界面截图** | 架构图参考 | 官方文档或 GitHub README | `fig/素材/screenshot_ui.png` | P1 |
| 3 | **ClawJacked 漏洞示意图** | 攻击路径图参考 | Oasis Security 报告 | `fig/素材/clawjacked_diagram.png` | P1 |

**人工搜索指引**：

1. **官网品牌资源**：访问 `https://openclaw.ai`，查找 Brand、Press Kit、Media、About 等页面，下载官方 Logo
2. **安全报告原图**：搜索 "ClawJacked Oasis Security report" 查找原始技术报告中的图表
3. **GitHub 组织页面**：`https://github.com/openclaw` 头像已下载备用

---

### 步骤 2：生成 AI 背景图（你需要执行）

使用外部 AI 绘图工具（Midjourney / Stable Diffusion）生成 7 张背景图，保存到 `fig/素材/`。

AI 提示词见下方「AI 绘图提示词」章节。

### 步骤 3：排版与合成

使用 `post-builder` 技能进行文字叠加和排版，输出最终定稿图到 `fig/定稿图/`。

---

## 人工素材搜索清单（你需要执行）

以下是需要你**人工搜索并下载**的素材，请在生成 AI 背景图之前完成：

### A. 品牌资产类

| 素材 | 搜索关键词 | 建议来源 | 保存路径 |
|------|-----------|----------|----------|
| OpenClaw 官方 Logo | `OpenClaw AI logo svg`、`OpenClaw brand assets` | 官网 `openclaw.ai/brand` 或 GitHub 组织页 | `fig/素材/logo_openclaw.svg` |

### B. 参考图类

| 素材 | 搜索关键词 | 建议来源 | 保存路径 |
|------|-----------|----------|----------|
| 应用界面截图 | `OpenClaw UI screenshot`、`OpenClaw dashboard` | 官方文档、GitHub README | `fig/素材/screenshot_ui.png` |
| ClawJacked 漏洞图 | `ClawJacked vulnerability diagram`、`Oasis Security OpenClaw` | Oasis Security 报告、TheHackerNews | `fig/素材/clawjacked_diagram.png` |

### C. 执行方式

1. **浏览器搜索**：使用 Google/ Bing 搜索上述关键词
2. **保存图片**：右键保存图片到 `fig/素材/` 目录
3. **命名规范**：按照建议路径命名，方便后续排版

---

## AI 绘图提示词（外部生图使用）

> 说明：以下提示词用于 Midjourney / Stable Diffusion 等 AI 绘图工具。生成后保存至 `fig/素材/` 目录，命名格式：`AI_01_cover.png`、`AI_02_architecture.png` 等。

---

### AI_01_cover - 封面背景图

**用途**：封面背景，后续叠加 OpenClaw Logo 和标题文字

**Prompt (Midjourney)**：
```
/imagine prompt: minimalist tech illustration, a menacing robotic claw emerging from dark digital void, glowing red warning light at the tip, abstract network connections in deep background, cyber security threat concept, dark noir style, deep blacks (#0D0D0D) and red accents (#DC2626), dramatic centered lighting, clean composition with negative space for text overlay, 3:4 aspect ratio --ar 3:4 --stylize 250 --v 6
```

**Prompt (Stable Diffusion)**：
```
masterpiece, best quality, cyber security illustration, robotic claw from darkness, glowing red warning light, digital network background, tech noir, deep black background, red accent lighting, dramatic shadows, minimalist, clean composition, negative space, --ar 3:4
Negative prompt: text, watermark, logo, blurry, low quality, cluttered, busy
```

**保存路径**：`fig/素材/AI_01_cover.png`
**尺寸要求**：3000x4000 (3:4)

---

### AI_02_architecture_bg - 架构图背景

**用途**：架构图解的背景底图（架构图本身用排版工具叠加）

**Prompt (Midjourney)**：
```
/imagine prompt: abstract technology diagram background, dark gradient from black to deep blue, subtle network node patterns in corners, clean central area for diagram overlay, cyber security aesthetic, minimal geometric elements, professional tech presentation style, 16:9 aspect ratio --ar 16:9 --stylize 100 --v 6
```

**Prompt (Stable Diffusion)**：
```
masterpiece, best quality, tech diagram background, dark gradient black to blue, subtle network patterns, clean center, cyber security aesthetic, geometric elements, professional style, --ar 16:9
Negative prompt: text, watermark, busy patterns, cluttered, foreground elements
```

**保存路径**：`fig/素材/AI_02_architecture_bg.png`
**尺寸要求**：1920x1080 (16:9)

---

### AI_03_timeline_bg - 时间线背景

**用途**：安全事件时间线的背景底图

**Prompt (Midjourney)**：
```
/imagine prompt: horizontal timeline background, dark cyber security theme, subtle red alert glow on left and right edges, clean dark center area, abstract digital grid pattern, professional infographic style, deep black (#0D0D0D) with faint red (#DC2626) accents, 21:9 ultrawide format for horizontal timeline --ar 21:9 --stylize 150 --v 6
```

**Prompt (Stable Diffusion)**：
```
masterpiece, best quality, horizontal timeline background, dark cybersecurity theme, red alert glow edges, clean dark center, digital grid pattern, professional infographic, deep black with red accents, ultrawide format, --ar 21:9
Negative prompt: text, watermark, busy, cluttered, foreground objects
```

**保存路径**：`fig/素材/AI_03_timeline_bg.png`
**尺寸要求**：4200x1800 (21:9 横向)

---

### AI_04_attack_flow - 攻击流程图背景

**用途**：ClawJacked 攻击路径流程图的背景

**Prompt (Midjourney)**：
```
/imagine prompt: vertical flowchart background, cyber security alert theme, dark gradient top to bottom, subtle warning triangle patterns faded in background, clean vertical path for flow arrows, professional tech infographic style, deep black to dark red gradient, 3:4 aspect ratio --ar 3:4 --stylize 150 --v 6
```

**Prompt (Stable Diffusion)**：
```
masterpiece, best quality, vertical flowchart background, cybersecurity alert, dark gradient top to bottom, faded warning patterns, clean vertical path, professional infographic, black to dark red gradient, --ar 3:4
Negative prompt: text, watermark, arrows, busy patterns, foreground elements
```

**保存路径**：`fig/素材/AI_04_attack_flow_bg.png`
**尺寸要求**：3000x4000 (3:4)

---

### AI_05_risk_matrix - 风险矩阵背景

**用途**：风险对比表格的背景底图

**Prompt (Midjourney)**：
```
/imagine prompt: data table background, dark professional tech style, subtle grid lines visible, clean cells for data entry, cyber security dashboard aesthetic, deep black background with faint blue grid, minimalist corporate tech, 16:10 aspect ratio --ar 16:10 --stylize 100 --v 6
```

**Prompt (Stable Diffusion)**：
```
masterpiece, best quality, data table background, dark professional tech, subtle grid lines, clean cells, cybersecurity dashboard, deep black with faint blue grid, minimalist, --ar 16:10
Negative prompt: text, watermark, data, numbers, busy
```

**保存路径**：`fig/素材/AI_05_risk_matrix_bg.png`
**尺寸要求**：3200x2000 (16:10)

---

### AI_06_checklist - 防护清单背景

**用途**：防护清单 Checklist 的背景

**Prompt (Midjourney)**：
```
/imagine prompt: checklist background, dark professional tech aesthetic, subtle checkbox outlines on left side, clean list area, cyber security briefing style, deep black background with faint gray lines, minimalist design, 3:4 aspect ratio --ar 3:4 --stylize 100 --v 6
```

**Prompt (Stable Diffusion)**：
```
masterpiece, best quality, checklist background, dark professional tech, subtle checkbox outlines, clean list area, cybersecurity briefing, deep black with faint gray lines, minimalist, --ar 3:4
Negative prompt: text, watermark, filled checkboxes, busy patterns
```

**保存路径**：`fig/素材/AI_06_checklist_bg.png`
**尺寸要求**：3000x4000 (3:4)

---

### AI_07_summary_card - 核心论点卡片背景

**用途**：6 条核心论点总结卡片的背景

**Prompt (Midjourney)**：
```
/imagine prompt: quote card background, dark minimalist tech style, subtle gradient from black to deep charcoal, clean centered area for text, professional presentation aesthetic, cyber security report style, deep black (#0D0D0D) to gray (#1F1F1F) gradient, 3:4 aspect ratio --ar 3:4 --stylize 100 --v 6
```

**Prompt (Stable Diffusion)**：
```
masterpiece, best quality, quote card background, dark minimalist tech, subtle gradient black to charcoal, clean center, professional presentation, cybersecurity report style, --ar 3:4
Negative prompt: text, watermark, logo, busy patterns, foreground objects
```

**保存路径**：`fig/素材/AI_07_summary_card_bg.png`
**尺寸要求**：3000x4000 (3:4)

---

## AI 生图统一参数建议

| 参数 | Midjourney | Stable Diffusion |
|------|------------|------------------|
| 比例 | 按各图要求 `--ar` | 按各图要求 `--ar` |
| 风格化 | `--stylize 100-250` | CFG Scale: 7 |
| 版本 | `--v 6` | 推荐 SDXL 或 MJ v6 模型 |
| 采样步数 | - | 30-50 steps |

---

## 生图后处理建议

1. **文字叠加**：使用 post-builder 或 Canva/PS 在背景图上叠加中文文字
2. **统一色调**：确保所有图片色调一致（深黑 + 暗红 + 科技蓝）
3. **文字规范**：使用无衬线字体（思源黑体/苹方），标题加粗
4. **留白检查**：确保文字区域有足够对比度和留白
