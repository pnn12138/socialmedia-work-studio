# 内容组装师技能

## 技能描述

此技能调用 post-builder agent 执行视觉规划的图片需求，整合素材生成平台适配发布稿。

## 使用方式

```
/run-post-builder [选题名称] [--platform=xiaohongshu,toutiao,wechat]
```

## 输入要求

- 必须存在 `topics/{topic-name}/post.md` 母稿
- 必须存在 `topics/{topic-name}/fig/visual_plan.md` 且状态为「精修版已完成」
- 必须存在 `topics/{topic-name}/fig/素材/` 目录 containing 所需素材

**重要**：post-builder 基于 `visual_plan.md` 中的「图片执行脚本」执行，而不是独立的 `requirements.md`。

## 输出位置

```
topics/{topic-name}/
├── xiaohongshu.md    # 小红书版本
├── toutiao.md        # 今日头条版本（可选）
└── wechat.md         # 微信公众号版本（可选）

topics/{topic-name}/fig/
├── 原始素材/            # 原始图片素材
│   └── README.md       # 素材清单与来源
├── 定稿图/              # 最终选用图片
│   ├── 01_cover.jpg    # 封面
│   ├── 02_inner_01.jpg # 内页 1
│   └── README.md       # 使用说明
└── visual_plan.md      # 执行日志填写在此文件中
```

## 执行流程

### 1. 读取视觉规划

读取 `visual_plan.md` 中的「图片执行脚本」章节，理解每张图的：
- `purpose`、`theme_anchor`、`visual_goal`
- `must_have`、`must_avoid`
- `prompt / keywords`（如有）
- `获取方式`（existing / hybrid-edit / ai-generate / hybrid-ai）

### 2. 图片需求执行

按 `visual_plan.md` 中定义的获取方式逐项处理：

| 获取方式 | 执行动作 |
|----------|----------|
| `existing` | 验证现有素材，调用 image-compose-local 做必要处理，输出至定稿图/ |
| `hybrid-edit` | 调用 image-compose-local 进行裁剪拼贴 + 加字，输出至定稿图/ |
| `ai-generate` | 用户在外部工具生成，post-builder 负责后处理与筛选 |
| `hybrid-ai` | 素材与 AI 生成图结合，调用 background-remover 等技能处理 |

### 3. 填写执行日志

**必须在 `visual_plan.md` 的「执行日志」章节中填写每张图的执行记录**：

```markdown
### 01_cover
- 原始素材：fig/素材/logo_openclaw_favicon.svg
- 执行方式：hybrid-edit（素材裁剪 + 文字叠加）
- 做了哪些优化：
  - 调整 Logo 位置至视觉中心
  - 增加红色外发光强化警示感
  - 叠加主副标题文字
- 为什么选这一版：Logo 居中构图最稳定，红色强调与主题色一致
- 输出文件：fig/定稿图/01_cover.jpg
- 尺寸：1242x1660
```

### 4. 发布稿生成

整合母稿与图片，生成平台适配内容：
- 标题（符合平台规范）
- 正文（平台适配格式）
- 标签列表
- 图片引用说明

## 输出内容

### 平台适配稿

| 平台 | 文件名 | 说明 |
|------|--------|------|
| 小红书 | `xiaohongshu.md` | 默认生成 |
| 今日头条 | `toutiao.md` | 可选 |
| 微信公众号 | `wechat.md` | 可选 |

### 发布素材包

```
topics/{topic-name}/publish/
├── README.md          # 发布清单
├── content/           # 各平台正文
├── images.md          # 图片引用清单
└── schedule.md        # 发布建议时间
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--platform` | 指定生成平台 | xiaohongshu |
| 多个平台用逗号分隔 | 如 `--platform=xiaohongshu,toutiao` | - |

## 注意事项

- 图片总数不超过 5 张
- 必须在 `visual_plan.md` 中填写执行日志，而不是单独创建文件
- 使用 image-finder 的图片需记录来源与授权
- 每张图处理后需用户确认才能进入下一张
- 全部执行完成后通知 visual-post-reviewer 进行审核

## 与 visual-post-reviewer 的交接

执行完成后：
1. 确保 `visual_plan.md` 中「执行日志」填写完整
2. 确保 `定稿图/` 目录包含所有定稿图
3. 通知用户可进入审核流程
4. visual-post-reviewer 将在 `visual_plan.md` 的「审核意见」章节填写审核结果
