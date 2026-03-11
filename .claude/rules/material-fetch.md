# 素材获取规则 (Material Fetch Rules)

## 规则目的

定义素材获取的质量标准和操作规范，确保获取的素材符合项目要求。

---

## 素材质量标准

### Logo 质量标准

| 等级 | 格式 | 分辨率 | 说明 |
|------|------|--------|------|
| **S** | SVG | 任意 | 最佳 - 可无限缩放 |
| **A** | PNG | ≥512x512 | 优秀 - 高分辨率 |
| **B** | PNG | ≥256x256 | 良好 - 可用 |
| **C** | PNG/JPG | ≥128x128 | 勉强可用 |
| **D** | 任意 | <128x128 | 不推荐，需人工替换 |

### 评分公式

```
质量分 = 格式分 + 分辨率分 + 附加分

格式分:
- SVG: 100
- PNG: 80
- WEBP: 70
- JPG: 50
- ICO: 30

分辨率分:
- ≥512px: 40
- ≥256px: 30
- ≥128px: 20
- <128px: 10

附加分:
- 透明背景：+20
- 文件<50KB: +10
- 官方来源：+10
```

---

## 爬取平台优先级

### P0 - 必执行

| 平台 | 说明 | 超时设置 |
|------|------|----------|
| GitHub | 项目仓库 | 30s |
| 官网首页 | 解析 favicon/meta | 30s |
| Clearbit | Logo API | 15s |
| Google Favicon | favicon 服务 | 15s |

### P1 - 条件执行

当 P0 未找到 SVG 或高质量 Logo 时执行：

| 平台 | 说明 | 超时设置 |
|------|------|----------|
| 官网子页面 | /brand, /press, /media | 60s |
| Brandfetch | 品牌 API | 30s |

### P2 - 备选方案

当前面都失败时执行：

| 平台 | 说明 | 超时设置 |
|------|------|----------|
| DuckDuckGo Images | 图片搜索 | 30s |
| Bing Images | 图片搜索 | 30s |

---

## 文件命名规范

```
格式：<type>_<source>_<identifier>[_<version>].<ext>

type:
- logo: Logo 文件
- icon: 图标文件
- screenshot: 截图
- asset: 其他素材

source:
- github: GitHub
- clearbit: Clearbit API
- google: Google Favicon
- brandfetch: Brandfetch
- official: 官网

identifier: 品牌名或项目名（小写，连字符）
```

**示例**：
- `logo_clearbit_openclaw.png`
- `logo_github_openclaw.svg`
- `icon_google_openclaw.ai.png`
- `screenshot_official_openclaw.png`

---

## 版权与合规

### 可使用素材

| 来源 | 商用 | 署名 | 说明 |
|------|------|------|------|
| GitHub 开源项目 | ✅ | 建议 | 遵循项目 LICENSE |
| 官网品牌资产 | ✅ | 通常需要 | 评论/分析属合理使用 |
| Clearbit Logo API | ✅ | 否 | 聚合公开数据 |
| Google Favicon | ✅ | 否 | 公开服务 |

### 限制使用素材

| 来源 | 限制 | 说明 |
|------|------|------|
| 小红书笔记图片 | ❌ 商用 | 仅学习参考 |
| 第三方图库 | 需验证 | 检查授权条款 |
| 品牌官方素材 | 需谨慎 | 避免商标侵权 |

---

## 人工核对触发条件

以下情况需要用户人工核对：

1. **质量不达标**
   - 最佳 Logo 质量分 < 80
   - 无 SVG 格式 Logo
   - 所有 Logo 分辨率 < 256px

2. **关键素材缺失**
   - 品牌 Logo 完全未找到
   - 缺少应用界面截图
   - 缺少品牌色参考

3. **来源可疑**
   - 非官方来源
   - 无法验证版权

---

## 重试策略

| 问题 | 重试动作 | 最大次数 |
|------|----------|----------|
| 无 SVG Logo | 爬取子页面 | 1 |
| 无高清 Logo | Brandfetch API | 1 |
| 官网 404 | Wayback Machine | 1 |
| GitHub 404 | 搜索镜像 | 1 |
| 所有来源失败 | 标记人工搜索 | - |

---

## 报告生成模板

见 `.claude/rules/material-fetch-report.md`
