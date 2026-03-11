# 素材获取报告模板 (Material Fetch Report)

## 报告结构

```markdown
# 素材获取报告 - {brandName}

**生成时间**: {timestamp}
**执行 Agent**: material-fetcher
**爬取平台数**: {platformCount}

---

## 执行摘要

- 爬取平台数：{platformCount}
- 获取素材总数：{totalCount}
- 最佳质量素材：{bestCandidate}
- 需要人工补充：{manualCount} 项

---

## ✅ 已获取素材清单

| 文件名 | 来源 | 格式 | 分辨率 | 质量评分 | 推荐用途 |
|--------|------|------|--------|----------|----------|
{logoTableRows}

---

## ⚠️ 低质量素材标记

以下素材质量较低，建议人工替换：

| 文件名 | 问题 | 建议 |
|--------|------|------|
{lowQualityRows}

---

## ❌ 未找到的素材

以下素材未能自动获取，需要人工搜索：

| 素材类型 | 建议搜索关键词 | 建议来源 |
|----------|---------------|----------|
{missingRows}

---

## 📋 人工搜索建议

### {taskIndex}. {taskName}
- **搜索词**: {keywords}
- **来源**: {sources}
- **保存路径**: `{savePath}`

---

## 下一步行动

1. [ ] 检查「低质量素材」是否需要替换
2. [ ] 按照「人工搜索建议」下载缺失素材
3. [ ] 完成后回复：`/material-fetcher confirm`

---

## 附录：执行日志

```
{executionLogs}
```
```

---

## 质量评分说明

| 评分 | 等级 | 说明 |
|------|------|------|
| 90-100 | S | 最佳 - 可直接使用 |
| 80-89 | A | 优秀 - 推荐使用 |
| 70-79 | B | 良好 - 可用 |
| 60-69 | C | 勉强可用 |
| <60 | D | 不推荐，建议人工替换 |

---

## 用户确认指令

```bash
# 确认素材满意，进入下一步
/material-fetcher confirm

# 需要补充特定素材
/material-fetcher add <type> <description>

# 重新评估（人工补充后）
/material-fetcher review

# 放弃当前素材，重新开始
/material-fetcher restart
```
