# 视觉规划师技能

## 技能描述

此技能调用 visual-planner agent 为内容选题生成视觉规划方案。

支持两种模式：
- **初版规划**：生成视觉策略 + 素材需求清单
- **精修版**：基于已获取素材生成详细执行方案（含 prompt）

## 使用方式

```
# 初版规划
/run-visual-planner [选题名称]

# 精修版（素材获取完成后）
/run-visual-planner [选题名称] --mode=refine
```

## 输入要求

- 必须存在 `topics/{topic-name}/post.md` 母稿文件
- 精修版要求 `topics/{topic-name}/fig/visual_plan.md` 中已有素材获取状态

## 输出位置

```
topics/{topic-name}/fig/visual_plan.md  # 唯一输出文件
```

**不再输出** `README.md`、`requirements.md`、`theme-map.md` 等分散文件。

## 输出内容

### 初版规划（默认模式）

生成 `visual_plan.md` 的以下内容：
1. **视觉策略总览**：主题摘要、视觉总原则
2. **素材获取状态表**：素材需求清单（空表，等待 material-fetcher 填充）
3. **图片结构总览**：7 张图的用途、information_role、获取方式（待规划）

**初版不输出详细 AI prompt**，只定义素材需求。

### 精修版（--mode=refine）

在已有 `visual_plan.md` 基础上：
1. **评估素材状态**：判断素材是否足够
   - 足够 → 进入步骤 2
   - 不足 → 输出「补充素材清单」，返回等待补充
2. **输出详细执行方案**：为每张图填写完整的执行脚本
   - `purpose`、`theme_anchor`、`text_binding`、`visual_goal`
   - `must_have`、`must_avoid`、`prompt / keywords`、`ratio`

**精修版必须输出详细 AI prompt**，供 post-builder 执行使用。

## 迭代机制

```
初版规划 → material-fetcher 填充素材状态 → 精修版评估
                                              ↓
                                    ┌─────────┴─────────┐
                                    │                   │
                                    ▼                   ▼
                              素材足够             素材不足
                                    ↓                   ↓
                              输出执行方案        输出补充清单
                                                    ↓
                                      material-fetcher 补充
                                                    ↓
                                           重新精修评估
```

**迭代触发条件**：
- 核心素材（Logo、关键截图）质量分 < 80
- 某张图无对应素材支撑
- 有关键素材缺失（标记为「⚪ 待获取」）

**迭代终止条件**：
- 所有核心素材质量分≥80
- 每张图都有素材支撑
- 无关键素材缺失

## 获取方式说明

visual-planner 为每张图指定以下获取方式之一：

| 方式 | 说明 | 执行者 |
|------|------|--------|
| `existing` | 直接用现有素材 | post-builder |
| `hybrid-edit` | 素材裁剪拼接 + 加字 | post-builder |
| `ai-generate` | 纯 AI 生成 | 用户外部生成 + post-builder |
| `hybrid-ai` | 素材+AI 结合生成 | 用户外部生成 + post-builder |

## 注意事项

- 图片总数默认 3–5 张，没有强理由不超过 5 张
- 初版规划不输出详细 prompt
- 精修版必须输出详细 prompt
- 必须在素材足够后才输出执行方案
- 所有状态记录在 `visual_plan.md` 单一文件中
