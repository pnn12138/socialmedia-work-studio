# 内容生产工作流技能

## 技能描述

此技能触发完整的 AI 自媒体内容生产流程：

```
trend-researcher → canonical-writer → visual-planner → post-builder → publisher
```

## 使用方式

```
/content-workflow [选题名称]
```

## 流程说明

### 1. trend-researcher（趋势研究员）
- 输入：用户提供的选题方向/链接/素材
- 输出：选题简报、趋势分析、对标信息

### 2. canonical-writer（母稿写作者）
- 输入：选题简报、核验后的信息
- 输出：平台无关的标准母稿

### 3. visual-planner（视觉规划师）
- 输入：母稿内容
- 输出：图片规划方案、AI 绘图 prompt

### 4. post-builder（内容组装师）
- 输入：母稿 + 视觉规划
- 输出：平台适配的完整发布稿

### 5. publisher（发布执行）
- 输入：审核通过的发布稿
- 输出：执行发布动作（需用户确认）

## 输入要求

最小输入：
- 一个选题方向或主题

可选输入：
- 参考链接
- 对标内容
- 用户补充观点
- 目标平台偏好

## 输出位置

完成后，内容位于：

```
topics/{topic-name}/
├── post.md           # 母稿
├── fig/
│   └── README.md     # 视觉规划
├── xiaohongshu.md    # 小红书版本
├── toutiao.md        # 今日头条版本（可选）
└── wechat.md         # 微信公众号版本（可选）
```

## 注意事项

1. 每个环节都会等待用户确认后再继续
2. 发布动作需要用户明确授权
3. 可在任意环节暂停或修改
