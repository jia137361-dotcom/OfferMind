# OfferMind 职引 — 用户端前端重设计

**日期**: 2026-05-20
**设计方式**: 渐进增强 (Approach C)
**后端改动**: 零，全部复用现有 API

---

## 1. 页面结构与路由

```
未登录:
  /              → Landing Page (产品介绍，纯静态)
  /login         → 登录
  /register      → 注册

已登录:
  /dashboard     → 工作台 (统计卡片 + 快捷入口 + 面试列表)
  /interview/new → 新面试 (快速模式 | Agent 智能模式，Tab 切换)
  /interview/:id → 面试答题 (对话流 + 评分卡片)
  /report/:id    → 面试报告 (总分大卡 + 三栏 + 逐题进度条)
  /profile       → 个人中心
```

---

## 2. Landing Page (/)

**路由**: `/` (未登录)
**类型**: 纯静态页面

**布局**:
- Navbar: OfferMind 职引 + 登录/注册
- Hero 区: 渐变背景 + 主标题 / 副标题 + CTA (免费体验 → 跳转 /register)
- 功能亮点区: 6 个卡片 3x2 网格
  - 上传简历 (AI 解析分析)
  - AI 岗位匹配 (Agent 自动匹配)
  - 模拟面试 (逐题作答)
  - 实时反馈 (SSE 流式评分)
  - 面试报告 (综合评估)
  - RAG 题库 (语义检索)
- Footer

**API**: 无

---

## 3. Dashboard 工作台 (/dashboard)

**路由**: `/dashboard` (已登录)
**数据来源**: `GET /api/v1/interviews` (已有)

**布局**:
- 个性化问候
- 统计卡片 (全部/进行中/已完成/平均分)，前端计算
- 快捷操作: 新面试 / Agent 智能匹配(跳 /interview/new Agent Tab) 
- 最近面试列表 (5条)，每项: 岗位 + 状态 + 难度/题数 + 日期 + 操作按钮

**API**: 1 个 (已有)

---

## 4. 新面试页 (/interview/new)

**路由**: `/interview/new` (已登录)
**数据来源**: `GET /api/v1/resumes` (已有), `POST /api/v1/interviews/start` (已有), `POST /api/v1/interviews/agent-setup` (已有)

**布局**: 两个 Tab
- Tab 1 "快速开始": 
  - 简历下拉选择 / 上传新简历
  - 目标岗位输入
  - 难度 (easy/medium/hard) + 题数 (3/5/8) 选择
  - 开始面试按钮 → `POST /api/v1/interviews/start`
- Tab 2 "Agent 智能匹配":
  - 说明区域: AI 自动分析简历 + 匹配岗位
  - 简历下拉选择
  - 开始智能面试按钮 → `POST /api/v1/interviews/agent-setup`
- 两个模式成功后都跳转 `/interview/:id`

**API**: 3 个 (全部已有)

---

## 5. 面试答题页 (/interview/:id)

**路由**: `/interview/:id` (已登录)
**数据来源**: `GET /api/v1/interviews/{id}/messages` (已有), `POST /api/v1/interviews/{id}/answer` (已有)

**布局**:
- 顶部: 返回按钮 + 进度条 (第 X/Y 题) + 难度
- 聊天区: 对话流气泡
  - 面试官气泡 (左侧，浅色背景 + AI 头像)
  - 候选人气泡 (右侧，渐变背景)
  - 每答完一题弹出评分卡片:
    - 分数 (⭐ X.X) + 反馈文字 + 关键得分点覆盖数 (X/Y 已覆盖)
- 底部: 输入框 + 发送按钮 + 提示文字
- 最后一题答完 → 自动跳转 `/report/:id`

**SSE 流式**: 保持现有实现。AI 反馈逐字出现，JSON 评分块解析后弹出评分卡片。

**API**: 2 个 (全部已有)

---

## 6. 面试报告 (/report/:id)

**路由**: `/report/:id` (已登录)
**数据来源**: `GET /api/v1/interviews/{id}/report` (已有)

**布局**:
- 顶部: 返回按钮
- 总分区: 圆形分数 + 等级 + 录用建议 + 岗位/难度/日期
- 总体评价: 文字摘要
- 三栏: 优势 / 待改进 / 建议
- 逐题回顾: 每项 Q + 分数 + 进度条可视化
- 底部: 再来一次 / 查看记录 按钮

**API**: 1 个 (已有)

---

## 7. 个人中心 (/profile)

保持现有功能，样式现代化。不展开。

---

## 文件改动清单

| 文件 | 动作 |
|------|------|
| `router/index.js` | 修改: 新增 / 和 /interview/new 路由 |
| `App.vue` | 修改: 导航栏双模式 (未登录/已登录) |
| `views/Landing.vue` | 新增 |
| `views/InterviewNew.vue` | 新增 |
| `views/Dashboard.vue` | 改造 |
| `views/Interview.vue` | 改造 (评分卡片) |
| `views/Report.vue` | 改造 (总分卡+进度条) |
| `views/Register.vue` | 微调样式 |
| `views/Profile.vue` | 微调样式 |
| `style.css` | 微调 |
| `api/resume.js` | 确认 getResumes 存在 |
| `api/interview.js` | 确认 agentSetup 存在 |

---

## 自检

- 无占位符，无不完整章节
- 所有页面与后端 API 一一对应，无新接口需求
- 8 个文件改动，2 个新文件
- 路由变更: 新增 2，无删除 (ResumeUpload 保留但不导航)
- 导航栏逻辑变更: App.vue 需判断未登录/已登录显示不同导航
