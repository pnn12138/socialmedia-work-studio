# .claude/skills 配置

此目录为 Claude Code 技能定义目录。

## 架构设计

本仓库采用四层架构进行视觉内容生产：

```
平台调度层 (xhs-adapter)
    ↓
视觉规划层 (visual-planner)
    ↓
图像生成层 (image-card-builder / asset-sourcer)
    ↓
视觉审查层 (visual-reviewer)
```

## 目录结构

```
.claude/skills/
├── README.md              # 本文件，技能总览
├── CLAUDE.md              # 本文件，技能配置说明
├── content-workflow/      # 内容生产工作流
│   └── SKILL.md
├── visual-planner/        # 视觉规划层（新建）
│   └── SKILL.md
├── image-card-builder/    # 图像生成层核心（新建）
│   └── SKILL.md
├── asset-sourcer/         # 素材补充能力（新建）
│   └── SKILL.md
├── visual-reviewer/       # 视觉审查层（新建）
│   └── SKILL.md
├── run-visual-planner/    # 视觉规划技能（旧版，保留兼容）
│   └── SKILL.md
├── run-post-builder/      # 内容组装技能（旧版，保留兼容）
│   └── SKILL.md
├── image-finder/          # 图片素材检索（已整合至 asset-sourcer）
│   ├── SKILL.md
│   └── ...
├── material-fetcher/      # 素材获取模块（已整合至 asset-sourcer）
│   ├── SKILL.md
│   └── ...
├── image-compose-local/   # 本地图像合成（能力已整合至 image-card-builder）
│   └── SKILL.md
├── image-builder/         # 图像生成编排（能力已整合至 image-card-builder）
│   └── SKILL.md
├── web-screenshot-capture/ # 网页截图（能力已整合至 asset-sourcer）
│   └── SKILL.md
├── background-remover/    # 背景移除
│   └── SKILL.md
├── cover-layout-maker/    # 封面排版
│   └── SKILL.md
├── image-export-qc/       # 导出质检
│   └── SKILL.md
├── smart-cropper/         # 智能裁剪
│   └── SKILL.md
└── xiaohongshu-mcp-skills/ # 小红书 MCP 技能集合
    └── ...
```

## 技能注册

技能通过 `SKILL.md` 文件进行定义，Claude Code 会自动识别此目录下的技能。

## 使用方式

1. 在对话中输入 `/skills` 打开技能选择器
2. 或直接输入 `/技能名` 调用技能

## 核心工作流

### 完整图像生产流程

```
用户请求 -> xhs-adapter(平台调度)
              ↓
      visual-planner(视觉规划)
              ↓
      asset-sourcer(素材获取，如需)
              ↓
      image-card-builder(图像渲染)
              ↓
      visual-reviewer(视觉审查)
              ↓
         发布包输出
```

### 简单图像需求

如只需要单张图或已有明确 spec：

```
用户请求 -> image-card-builder(直接渲染)
```

### 仅需素材

如只需要获取素材：

```
用户请求 -> asset-sourcer(素材获取)
```

## 技能开发

参考 `content-workflow/SKILL.md` 作为模板。

## 技能迁移说明

| 旧技能 | 新技能 | 说明 |
|--------|--------|------|
| `run-visual-planner` | `visual-planner` | 新版视觉规划，输出 visual_plan.md |
| `run-post-builder` | `post-builder` | 内容组装，已整合图像执行能力 |
| `image-builder` + `image-compose-local` | `image-card-builder` | 整合为统一图像渲染能力 |
| `image-finder` + `material-fetcher` + `web-screenshot-capture` | `asset-sourcer` | 整合为统一素材获取能力 |

旧版技能保留兼容，但新任务建议优先使用新版技能。
