# Claude Code 图像能力升级框架文档

## 1. 目标与设计原则

本框架用于在 Claude Code 项目内搭建一套可维护、可复用、可扩展的图像生产能力，服务于小红书图文内容生产。目标不是做一个“什么都会的超大 agent”，而是建立一条清晰的视觉生产流水线，使 Claude Code 能够稳定完成以下任务：理解一篇内容需要哪些图、判断哪些图可以直接绘制、判断哪些图需要外部素材、用统一模板生成图像、对生成结果进行基本审美审查，并将所有结果按项目规范写回到对应目录中。

整体设计遵循五个原则。第一，平台适配与制图能力分离，小红书 adapter 只负责平台层决策，不直接承载绘图实现。第二，优先模板化而不是一次性生成，优先用 HTML/CSS、SVG 或脚本化渲染构建可复用模板。第三，优先直接绘制而不是先搜素材，对“标题卡、警示图、清单图、观点图、总结图”这类小红书常见样式，应尽量由 Claude Code 直接出图。第四，素材采集能力作为补充，而不是主干，只有当某张图确实依赖真实背景图、网页截图、产品图、logo 或实拍素材时，才进入 asset-sourcer 链路。第五，输入输出必须结构化，每个阶段都要有明确的输入文件、输出文件与目录落点，避免 agent 自由发挥导致结果不可控。

## 2. 总体架构

建议采用四层结构：平台调度层、视觉规划层、图像生成层、视觉审查层。

平台调度层由 `xiaohongshu-adapter` 承担。它读取选题、正文、章节结构和平台要求，决定需要多少张图、每张图的用途是什么，并调用下游 skills 完成生成。

视觉规划层由 `visual-planner` 承担。它负责把“文章内容”转化成“图像任务列表”，输出标准化的图片需求文件，例如 `fig/specs/*.json`。它不直接画图，也不负责找素材。

图像生成层拆成两条路径。第一条是 `image-card-builder`，用于直接生成可模板化的小红书图，例如封面图、观点图、警示图、列表图、对比图、时间线图。第二条是 `asset-sourcer`，用于补充外部素材，如背景图、图标、网页截图、logo 等，然后再交给 `image-card-builder` 或后续 builder 做合成。

视觉审查层由 `visual-reviewer` 承担。它用于在图片生成后进行结构化检查，包括信息层级是否清晰、标题是否过长、画面是否像素材堆砌、是否符合小红书用户常见阅读习惯，以及是否与正文重点一致。

因此，推荐的主流程不是固定的三段，而是：

`xiaohongshu-adapter -> visual-planner -> route decision -> (image-card-builder 或 asset-sourcer + image-card-builder) -> visual-reviewer`

其中 `route decision` 可以由 adapter 自己完成，也可以由 planner 输出 `render_mode` 字段供 adapter 判断。

## 3. 能力边界与角色职责

### 3.1 xiaohongshu-adapter

这是平台层 agent，不是绘图器。它的职责是理解“小红书内容生产”这个平台场景，读取当前选题草稿，识别内容结构，决定图片数量和作用，并把图片任务写成结构化 spec 或发给相应 skill。它不负责具体画图细节，不直接写 HTML 模板，不直接操作 Playwright，也不自己处理外部素材下载。它的核心价值在于“平台理解”和“任务分发”。

它应该完成以下工作：读取文章草稿与选题信息；按照小红书图文习惯拆分图片节奏；判断每张图是封面、观点页、风险页、解释页还是总结页；调用 `visual-planner` 输出图片需求；根据 `render_mode` 调用 `image-card-builder` 或 `asset-sourcer`；调用 `visual-reviewer` 审核结果；将最终图片路径回写至帖子目录。

### 3.2 visual-planner

`visual-planner` 的职责是把文字结构翻译成视觉结构。输入通常是主题、标题、正文草稿、内容大纲、平台类型以及风格要求。输出应该是多张图片的 spec 列表，每个 spec 对应一张图。

每张图的 spec 至少应包含：`id`、`purpose`、`template`、`render_mode`、`aspect_ratio`、`title`、`subtitle`、`body`、`highlights`、`visual_tone`、`must_include`、`must_avoid`、`asset_needs`、`notes_for_builder`。如果一张图需要素材，应写明 `asset_needs` 的类型，例如背景图、网页截图、科技感纹理、logo、警示 icon；如果一张图适合直接绘制，则 `render_mode` 应为 `direct`。

`visual-planner` 的输出必须足够具体，使后续 builder 不需要再做语义猜测。例如不能只写“做一张警示图”，而应写成“3:4 竖版，封面用途，主标题为‘致命 RCE 漏洞’，副标题为两行以内，整体风格为高危警示科技风，中央需要盾牌/警示元素，背景可为浅色科技线框，避免出现过多写实黑客形象”。

### 3.3 image-card-builder

这是最核心的 skill。它负责把 spec 渲染成图像。它应优先支持“文本主导型图片”，也就是你现在最需要的这类小红书图：白底黑字信息卡、漏洞警示封面、三点总结图、观点图、对比图、时间线图。

它内部应采用模板系统，而不是每次从零生成。推荐模板至少包括：`cover-alert`、`cover-minimal`、`cover-list`、`quote-card`、`compare-card`、`timeline-card`。这几个模板足以覆盖多数技术类小红书图文的视觉表达。

`image-card-builder` 的输入是单张图 spec；输出应至少包括：最终 PNG 文件、用于渲染的中间 HTML 或 SVG 文件、规范化后的 spec 备份文件、渲染日志。这样后续你可以追溯每张图是如何生成的，也便于二次修改。

### 3.4 asset-sourcer

这个 skill 不应默认参与所有图片生成。它只处理外部素材需求。它的职责包括：通过素材 API 搜索背景图或配图；下载图标；用浏览器脚本截取网页局部；将所有素材统一存入 `fig/assets/`；输出一份 `assets.json` 或更新后的 spec，供 builder 使用。

对于你这种以文字卡片为主的内容，`asset-sourcer` 应该被视为补充能力，而不是主干。只有以下情况才建议使用：需要真实照片背景、需要产品官网截图、需要某个开源项目页面的界面截图、需要某品牌或工具 logo、需要一张科技背景底图增强封面表现力。

### 3.5 visual-reviewer

`visual-reviewer` 的任务不是生成图片，而是扮演视觉编辑。它应对结果进行结构化审查，例如：标题是否过长导致拥挤、字号层级是否混乱、重点词是否过多、背景是否喧宾夺主、是否有明显的“AI 拼凑感”、是否符合小红书竖版阅读习惯、是否与正文重点一致。

它的输出可以分为两部分：审查结论和修改建议。若合格，返回“通过”；若不合格，明确指出需要减少的文字、需要替换的模板、需要增强的主视觉元素或需要重新获取的素材类型。

## 4. 为什么建议做成 skills，而不是全塞进一个 agent

这套能力做成 skills 的好处非常明显。首先，复用性更高。你今天给小红书 adapter 用，后面公众号封面生成器、即刻卡片生成器、PPT 封面构建器都可以复用同一套 `image-card-builder`。其次，易于测试。你可以单独输入一个 spec 测试 builder 的稳定性，而不必每次从全文内容开始跑完整链路。再次，便于替换底层实现。当前可以用 HTML/CSS + Playwright，以后如果想替换成 SVG + resvg 或 node-canvas，不需要动 adapter 和 planner。最后，便于排错。失败时你能明确知道是 planner 出 spec 有问题、asset-sourcer 没找到合适素材，还是 builder 的模板渲染失败，而不是在一个巨型 agent 里难以定位。

## 5. 推荐的底层技术路线

### 5.1 最推荐：HTML/CSS + Playwright 截图

对你当前的小红书图文场景，这是最推荐的主实现路线。原因是这类图的难点不在复杂插画，而在文字排版、字号层级、自动换行、留白、圆角、阴影、渐变背景、角标等卡片设计能力。HTML/CSS 天生擅长这些事情，Claude Code 也最容易稳定生成 HTML 模板和 CSS 样式。

实现方式是：`image-card-builder` 根据 spec 生成一份局部 HTML 或完整页面，再由 Playwright 打开本地页面并截图输出 PNG。这样做的优点是易于调试、适合中文、多模板可复用、方便后续做主题系统。尤其是 3:4 小红书竖版图，非常适合使用固定画布尺寸的 HTML 容器来渲染。

### 5.2 第二推荐：SVG + resvg-js

这条路线适合扁平化程度更高、矢量感更强的模板，例如流程图、科技卡片、榜单图、结构性较强的封面。它的优点是模板结构更清晰、渲染速度快、很适合版本管理和批量导出。对于“标题 + 副标题 + icon + 简单背景”的图，SVG 非常合适。

### 5.3 第三推荐：node-canvas

如果你后续需要一套不依赖浏览器环境的纯 Node 脚本出图方案，可以再补 node-canvas。它适合做固定模板批量生成、简单贴图、简单文本卡片。但从可维护性与前期速度来看，它不应是第一选择，因为复杂中文排版和样式管理会比 HTML/CSS 更麻烦。

## 6. 素材 API、工具、MCP、hooks 的建议

### 6.1 适合的素材 API

首先应接入免费且许可清晰的素材库 API，优先用于背景图和配图检索。最适合先落地的是 Pexels API，因为它提供图片和视频搜索能力，接口简单，适合快速搭建 `image-finder` 类 skill。若后续需要补充来源，可再考虑 Unsplash 等其他平台，但第一版没必要做得太宽。

对于图标类素材，不建议让 agent 在网页上乱找，应该优先使用固定图标库或本地 icon 资源。若只是锁头、盾牌、感叹号、聊天框、机器人等简单元素，更推荐直接在模板中用 SVG 绘制，而不是到处找 png。

### 6.2 适合的浏览器工具

浏览器自动化不应作为主绘图能力，而应作为素材补充能力。推荐将 Playwright 作为浏览器底座，因为它稳定、成熟、适合本地 HTML 渲染截图，也适合做网页局部截图。如果后续想让 agent 通过更自然语言化的方式控制浏览器，再评估 Stagehand 或其他 agent 化封装。但第一阶段没必要直接上“重 agent 浏览器”，先把 Playwright 用于两件事做扎实：本地模板截图、网页截图采集。

### 6.3 适合的 MCP

如果你的 Claude Code 环境已经接入 MCP，那么最值得接的是两类。第一类是文件系统与脚本执行相关的能力，用于渲染图片、保存文件、读取 spec。第二类是浏览器控制能力，用于 Playwright 截图或局部采集。如果你后续确实要让 Claude Code 能更自动地“打开某网站并抓取 hero 图”，可以再加浏览器类 MCP，但依然建议让其只为 `asset-sourcer` 服务，而不是让整个 adapter 依赖它。

### 6.4 适合的 hooks

hooks 的主要作用不是“代替 skill”，而是让流程自动化。推荐至少设置三种 hook。第一种是 spec 生成后的校验 hook，当 `fig/specs/` 下生成新 spec 时，自动检查字段是否完整，缺字段就报错。第二种是 builder 输出后的预览 hook，当 `fig/output/` 下生成新图片时，自动更新一个 `README.md` 或 gallery 文件，方便人工快速查看。第三种是审查 hook，当某次渲染完成后，自动调用 `visual-reviewer` 生成简单审查结论，写入旁边的 review 文件。

## 7. 推荐目录结构

建议以“skills 放在 Claude 规则目录，具体帖子放在项目目录”的方式组织。

```text
.claude/
  skills/
    visual-planner/
      SKILL.md
      examples/
      schemas/
    image-card-builder/
      SKILL.md
      templates/
        cover-alert/
        cover-minimal/
        cover-list/
        quote-card/
        compare-card/
        timeline-card/
      scripts/
        render-card.js
        render-html.js
      examples/
    asset-sourcer/
      SKILL.md
      scripts/
        fetch-pexels.js
        capture-web.js
        collect-assets.js
      examples/
    visual-reviewer/
      SKILL.md
      checklists/

posts/
  <topic>/
    draft.md
    outline.md
    fig/
      README.md
      specs/
      assets/
      output/
      review/
```

这个目录结构的关键点在于：skills 是通用能力，`posts/<topic>/fig/` 是单篇内容的工作空间。这样以后切换选题时，skills 不动，只换 `posts/` 下的数据。

## 8. spec 设计建议

建议将每张图片的描述写成独立 JSON 文件。推荐字段如下：

```json
{
  "id": "cover-01",
  "purpose": "封面图",
  "template": "cover-alert",
  "render_mode": "direct",
  "aspect_ratio": "3:4",
  "title": "致命 RCE 漏洞",
  "subtitle": "OpenClaw 爆出高危问题",
  "body": [
    "一个恶意链接，可能直接接管电脑。",
    "别把高权限 Agent 默认运行当小事。"
  ],
  "highlights": ["RCE", "高危", "默认高权限"],
  "visual_tone": "高危警示、科技感、适合小红书封面",
  "must_include": ["警示感", "大标题", "中央视觉元素"],
  "must_avoid": ["信息过密", "背景过花", "低质黑客素材"],
  "asset_needs": [],
  "notes_for_builder": "整体留白充足，标题要强，正文不超过三段"
}
```

如果需要素材，可以把 `render_mode` 改为 `sourced`，并在 `asset_needs` 中写清楚，例如 `科技背景图`、`OpenClaw logo`、`网页截图`、`盾牌 icon`。

## 9. 模板系统设计建议

建议第一阶段只做最常用的四个模板，不要一开始就把所有模板做完。优先顺序如下：

首先是 `cover-alert`，用于高危漏洞、翻车、紧急提醒类内容。第二是 `cover-minimal`，用于大标题加正文的极简信息卡。第三是 `cover-list`，用于三点总结、五个结论、步骤式内容。第四是 `compare-card`，用于对比、优缺点、前后变化类内容。

当这四个模板稳定后，再考虑增加 `quote-card` 和 `timeline-card`。模板系统应该有统一的主题变量，例如字体、主色、强调色、背景色、圆角、阴影、边距、标题字号、正文行高等。这样 Claude Code 在新增模板时不会风格漂移太大。

## 10. 小红书 adapter 的工作逻辑建议

小红书 adapter 在一次任务中应遵循如下逻辑：先读取当前选题目录下的 `draft.md` 或 `outline.md`；识别文章的主题、重点、读者预期和情绪基调；调用 `visual-planner` 输出每张图的 spec；遍历所有 spec，根据 `render_mode` 决定调用路径；若为 `direct`，直接调 `image-card-builder`；若为 `sourced`，先调 `asset-sourcer` 获取素材，再把更新后的 spec 交给 `image-card-builder`；图片生成完成后，调用 `visual-reviewer`；若 reviewer 认为不合格，则进行一次修正循环，必要时替换模板或缩短文案；最终将成品图输出到 `fig/output/`，同时更新 `fig/README.md`，记录每张图的用途、路径和简短审查结论。

## 11. 分阶段升级路线

第一阶段只做最小可用闭环。目标是让 Claude Code 能从一个 spec 直接生成一张小红书风格图片，并写回到指定目录。这一阶段只需要完成 `image-card-builder`，底层采用 HTML/CSS + Playwright，模板只做 `cover-alert` 和 `cover-minimal` 两个。

第二阶段补齐 `visual-planner`。这时 Claude Code 就可以从文章草稿自动产出多张图的 spec，而不需要你手工一张张写。

第三阶段接入 `asset-sourcer`。这时一些需要背景图或网页截图的封面就能自动完成，不再局限于纯文字卡片。

第四阶段加入 `visual-reviewer` 和 hooks。这样流程从“能出图”升级为“能出图并做基本审美把关”。

第五阶段再考虑浏览器 agent 增强、更多模板、批量导出、多平台 adapter 复用。不要在第一阶段就把浏览器 agent、素材 API、复杂拼图和视觉审查全部混在一起做，否则 Claude Code 很容易把工程做得太散。

## 12. 对 Claude Code 的实施要求

Claude Code 在实现这套框架时，应遵循以下要求：所有输入输出文件路径必须清晰；每个 skill 目录必须包含 `SKILL.md`；渲染脚本要可单独执行；模板必须可扩展；生成的图片必须留存对应 spec；目录中必须有示例输入和示例输出；同一张图片的失败日志要可追踪；不得在无 spec 的情况下自由发挥生成图片；若缺少素材或字段，应明确报错而不是静默生成低质量结果。

## 13. 最终建议

对你当前的项目，不应先追求“全自动搜图 agent”，而应先把“小红书图像模板化直接绘制能力”打牢。因为你现在最常见、最高频、最有复用价值的图片，正是你刚才展示的这类文字主导型信息卡。它们最适合直接由 Claude Code 用模板生成，而不是依赖复杂的图像大模型或不稳定的网页搜索。

因此，当前最优顺序是：先做 `image-card-builder`，再补 `visual-planner`，然后接 `asset-sourcer`，最后加入 `visual-reviewer`。同时，将这些能力做成 skills，由小红书 adapter agent 统一调度。这样你的系统会更稳、更容易扩展，也更适合后面继续接公众号、即刻、Twitter 或其他平台的内容生产流程。

