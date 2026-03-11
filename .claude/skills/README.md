# .claude/skills

此目录存放可复用的技能定义，供 Claude Code 调用。

## 架构设计

本仓库采用四层架构进行视觉内容生产：

```
平台调度层 (xhs-adapter / toutiao-adapter / wechat-adapter)
    ↓
视觉规划层 (visual-planner)
    ↓
图像生成层 (image-card-builder / asset-sourcer)
    ↓
视觉审查层 (visual-reviewer)
```

## 技能列表

### 核心技能（新版）

| 技能 | 层级 | 说明 |
|------|------|------|
| `visual-planner` | 视觉规划层 | 将母稿翻译成视觉方案，输出 visual_plan.md |
| `image-card-builder` | 图像生成层 | 将 spec 渲染成图像，支持模板化渲染 |
| `asset-sourcer` | 素材补充能力 | 获取外部素材（背景图、截图、logo 等） |
| `visual-reviewer` | 视觉审查层 | 审核图文成品质量，输出修改意见 |

### 平台适配器（Agents）

| Agent | 说明 |
|-------|------|
| `xhs-adapter` | 小红书平台调度层，统筹图像生产全流程 |
| `toutiao-adapter` | 今日头条适配器 |
| `wechat-adapter` | 微信公众号适配器 |

### 遗留技能（保留兼容）

| 技能 | 新技能 | 说明 |
|------|--------|------|
| `run-visual-planner` | `visual-planner` | 旧版视觉规划 |
| `run-post-builder` | `post-builder` | 旧版内容组装 |
| `image-builder` | `image-card-builder` | 已整合 |
| `image-compose-local` | `image-card-builder` | 已整合 |
| `image-finder` | `asset-sourcer` | 已整合 |
| `material-fetcher` | `asset-sourcer` | 已整合 |
| `web-screenshot-capture` | `asset-sourcer` | 已整合 |

## 技能调用方式

在对话中使用 `/skills` 查看可用技能。

或使用命令语法：

```
/技能名称 [参数]
```

## 核心工作流

### 完整图像生产流程（推荐）

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

## 技能开发规范

每个技能应包含：

1. `SKILL.md` - 技能定义与使用说明
2. 相关配置文件（如需）
3. 示例用法（如需）

## 与 agents 的关系

- `agents/` - 定义 AI 代理角色与职责
- `skills/` - 定义可重复执行的技能动作

一个 skill 可以调用多个 agent 来完成复杂任务。
