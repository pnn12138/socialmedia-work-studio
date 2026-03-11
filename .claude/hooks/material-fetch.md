# 素材获取钩子 (Material Fetch Hooks)

## 钩子目的

定义素材获取流程中的自动化触发器和后置处理。

---

## 前置钩子 (Pre-Hooks)

### hook:before-fetch

**触发时机**: 开始素材获取前

**执行动作**:
1. 解析目标（品牌名/项目名/URL）
2. 提取 domain、githubRepo 等信息
3. 检查输出目录是否存在
4. 创建临时工作目录

```json
{
  "event": "before-fetch",
  "handler": "prepare-fetch-context",
  "context": {
    "brandName": "{brandName}",
    "domain": "{domain}",
    "githubRepo": "{githubRepo}",
    "outputDir": "{outputDir}",
    "tempDir": "{tempDir}"
  }
}
```

---

### hook:before-crawl

**触发时机**: 爬取每个平台前

**执行动作**:
1. 检查平台可用性
2. 设置超时
3. 记录开始时间

```json
{
  "event": "before-crawl",
  "handler": "prepare-crawl-platform",
  "platform": "{platform}",
  "timeout": "{timeout}"
}
```

---

## 后置钩子 (Post-Hooks)

### hook:after-fetch

**触发时机**: 单个平台爬取完成后

**执行动作**:
1. 验证下载文件
2. 记录成功/失败
3. 更新进度

```json
{
  "event": "after-fetch",
  "handler": "process-fetch-result",
  "result": {
    "platform": "{platform}",
    "success": "{success}",
    "filesCount": "{filesCount}"
  }
}
```

---

### hook:after-all-fetch

**触发时机**: 所有平台爬取完成后

**执行动作**:
1. 聚合所有结果
2. 触发质量评估
3. 生成报告草稿

```json
{
  "event": "after-all-fetch",
  "handler": "aggregate-results",
  "results": "{allResults}"
}
```

---

### hook:quality-check

**触发时机**: 质量评估完成后

**执行动作**:
1. 检查是否需要重试
2. 标记低质量素材
3. 生成人工任务列表

```json
{
  "event": "quality-check",
  "handler": "process-quality-result",
  "quality": {
    "hasSVG": "{hasSVG}",
    "maxResolution": "{maxResolution}",
    "bestScore": "{bestScore}",
    "needsRetry": "{needsRetry}"
  }
}
```

---

### hook:report-generated

**触发时机**: 报告生成完成后

**执行动作**:
1. 保存报告到文件
2. 通知用户核对
3. 等待用户确认

```json
{
  "event": "report-generated",
  "handler": "notify-user-review",
  "reportPath": "{reportPath}"
}
```

---

### hook:user-confirmed

**触发时机**: 用户确认素材后

**执行动作**:
1. 清理临时文件
2. 移动素材到最终目录
3. 更新项目状态

```json
{
  "event": "user-confirmed",
  "handler": "finalize-material",
  "finalDir": "{finalDir}"
}
```

---

## 钩子配置文件

```json
// .claude/hooks/material-fetch.json
{
  "hooks": [
    {
      "event": "before-fetch",
      "action": "prepare-fetch-context"
    },
    {
      "event": "before-crawl",
      "action": "prepare-crawl-platform"
    },
    {
      "event": "after-fetch",
      "action": "process-fetch-result"
    },
    {
      "event": "after-all-fetch",
      "action": "aggregate-results"
    },
    {
      "event": "quality-check",
      "action": "process-quality-result"
    },
    {
      "event": "report-generated",
      "action": "notify-user-review"
    },
    {
      "event": "user-confirmed",
      "action": "finalize-material"
    }
  ]
}
```

---

## 钩子与 Agent 协作

```
material-fetcher Agent
    ↓
before-fetch Hook → 准备上下文
    ↓
执行爬取任务
    ↓
after-fetch Hook → 处理结果
    ↓
质量评估
    ↓
quality-check Hook → 决定是否重试
    ↓
生成报告
    ↓
report-generated Hook → 通知用户
    ↓
用户确认
    ↓
user-confirmed Hook →  finalize
```
