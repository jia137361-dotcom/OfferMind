# AI 面试系统项目解析

## 项目结构总览

```
ai-interview/
├── ai-interview-admin/    # 后台管理系统
├── ai-interview-backend/  # 后端 API 服务
├── ai-interview-frontend/ # 用户前端界面
├── FastAPI核心知识点文档.md
├── 三大数据库核心知识点总结.md
└── 部署文档.md
```

---

## 一、ai-interview-admin（后台管理系统）

### 项目类型
**后台管理系统**，基于 Vue 3 + Vite 构建的前端项目。

### 核心结构

```
ai-interview-admin/
├── src/
│   ├── api/           # API 调用
│   │   ├── index.js
│   │   └── request.js
│   ├── router/
│   │   └── index.js
│   ├── stores/
│   │   └── auth.js
│   ├── views/
│   │   ├── Dashboard.vue
│   │   ├── InterviewDetail.vue
│   │   ├── Interviews.vue
│   │   ├── Login.vue
│   │   └── Users.vue
│   ├── App.vue
│   ├── main.js
│   └── style.css
├── dist/              # 构建产物
├── package.json
└── vite.config.js
```

### 主要功能

| 页面 | 功能 |
|------|------|
| **Login.vue** | 管理员登录 |
| **Dashboard.vue** | 管理仪表盘 |
| **Users.vue** | 用户管理（查看、管理用户） |
| **Interviews.vue** | 面试管理（查看所有面试） |
| **InterviewDetail.vue** | 面试详情（查看具体面试内容） |

### 技术栈

- **框架**：Vue 3
- **路由**：Vue Router 4
- **状态管理**：Pinia
- **HTTP 客户端**：Axios
- **构建工具**：Vite

### 作用
**后台管理系统**，供管理员使用：
- 管理系统用户
- 查看和管理所有面试记录
- 监控系统运行状态
- 处理等待列表申请

---

## 二、ai-interview-backend（后端 API 服务）

### 项目类型
**后端 API 服务**，基于 FastAPI 构建的 Python 后端项目。

### 核心结构

```
ai-interview-backend/
├── app/
│   ├── api/           # API 路由
│   │   ├── backoffice/ # 后台管理 API
│   │   │   └── v1/
│   │   └── client/     # 客户端 API
│   │       └── v1/
│   ├── core/          # 核心配置
│   │   ├── config.py
│   │   └── security.py
│   ├── db/            # 数据库
│   │   ├── base.py
│   │   └── session.py
│   ├── models/        # ORM 模型
│   │   ├── interview.py
│   │   ├── interview_message.py
│   │   ├── user.py
│   │   └── resume.py
│   ├── services/      # 业务逻辑
│   │   ├── client/
│   │   │   ├── ai_service.py
│   │   │   ├── interview_service.py
│   │   │   └── resume_service.py
│   │   └── common/
│   └── utils/         # 工具函数
├── main.py            # 应用入口
├── docker-compose.yml # 容器编排
└── requirements.txt   # 依赖
```

### 主要功能

| 模块 | 功能 |
|------|------|
| **认证模块** | 用户注册、登录、密码重置 |
| **简历模块** | 简历上传、解析、管理 |
| **面试模块** | 开始面试、提交回答、生成报告 |
| **AI 服务** | 题目生成、回答评估、音频转写 |
| **后台管理** | 用户管理、面试管理、等待列表 |

### 技术栈

- **Web 框架**：FastAPI（异步为主）
- **数据库**：SQLAlchemy 2.0 Async + asyncpg + PostgreSQL
- **缓存/队列**：Redis（redis.asyncio）
- **后台任务**：Celery（另存有 APScheduler 代码）
- **身份验证**：JWT（python-jose）
- **AI 集成**：DeepSeek/OpenAI 风格客户端；音频转写使用 whisper
- **文件处理**：pdfplumber、PyPDF2、python-docx、S3（boto3）

### 作用
**系统核心服务**，负责：
- 处理前端和管理端的 API 请求
- 与数据库交互存储数据
- 集成 AI 服务进行面试评估
- 管理后台任务和定时任务
- 提供安全的认证和授权

---

## 三、ai-interview-frontend（用户前端界面）

### 项目类型
**用户前端界面**，基于 Vue 3 + Vite 构建的前端项目。

### 核心结构

```
ai-interview-frontend/
├── src/
│   ├── api/           # API 接口调用
│   │   ├── auth.js
│   │   ├── interview.js
│   │   ├── request.js
│   │   ├── resume.js
│   │   └── user.js
│   ├── router/
│   │   └── index.js
│   ├── stores/
│   │   └── auth.js
│   ├── views/
│   │   ├── Dashboard.vue
│   │   ├── Interview.vue
│   │   ├── Login.vue
│   │   ├── Profile.vue
│   │   ├── Register.vue
│   │   ├── Report.vue
│   │   └── ResumeUpload.vue
│   ├── App.vue
│   ├── main.js
│   └── style.css
├── dist/              # 构建产物
├── package.json
└── vite.config.js
```

### 主要功能

| 页面 | 功能 |
|------|------|
| **Login.vue** | 用户登录 |
| **Register.vue** | 用户注册 |
| **Dashboard.vue** | 仪表盘（用户中心） |
| **ResumeUpload.vue** | 简历上传 |
| **Interview.vue** | AI 面试界面 |
| **Report.vue** | 面试报告 |
| **Profile.vue** | 用户个人资料 |

### 技术栈

- **框架**：Vue 3
- **路由**：Vue Router 4
- **状态管理**：Pinia
- **HTTP 客户端**：Axios
- **构建工具**：Vite

### 作用
**用户界面**，负责：
- 用户注册登录
- 简历上传和管理
- AI 面试体验
- 面试报告查看
- 个人资料管理

---

## 四、系统架构关系

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  管理端 (admin)  │ ──▶ │   后端服务      │ ──▶ │  数据库 (PostgreSQL) │
└─────────────────┘     │  (backend)      │     └─────────────────┘
                        └─────────────────┘
                              ▲
                              │
                        ┌─────────────────┐
                        │  用户端 (frontend) │
                        └─────────────────┘
```

### 数据流

1. **用户操作流程**：
   - 用户注册/登录 → 上传简历 → 开始面试 → 提交回答 → 查看报告

2. **管理员操作流程**：
   - 登录后台 → 查看用户列表 → 查看面试记录 → 管理系统配置

3. **后端处理流程**：
   - 接收 API 请求 → 业务逻辑处理 → AI 服务调用 → 数据存储/检索 → 返回响应

---

## 五、核心技术特点

### 1. 前后端分离
- 前端：Vue 3 + Vite
- 后端：FastAPI + 异步处理
- API 通信：RESTful 接口

### 2. AI 集成
- **DeepSeek/OpenAI**：用于面试题目生成和回答评估
- **Whisper**：用于音频转写（支持本地或外部服务）
- **流式响应**：SSE 实时返回 AI 评估结果

### 3. 数据库设计
- **PostgreSQL**：存储核心业务数据
- **JSONB**：存储结构化数据（如面试题目、评估报告）
- **异步 ORM**：SQLAlchemy 2.0 Async

### 4. 缓存与队列
- **Redis**：缓存、会话管理、消息队列
- **Celery**：后台任务处理（邮件发送、AI 分析）

### 5. 部署架构
- **Docker**：容器化部署
- **Docker Compose**：服务编排
- **Nginx**：反向代理

---

## 六、项目价值

### 对用户
- 提供 AI 模拟面试体验
- 帮助提升面试技能
- 获得详细的面试评估报告
- 简历智能分析和优化建议

### 对企业
- 人才评估工具
- 标准化面试流程
- 批量面试管理
- 数据驱动的招聘决策

---

## 七、技术亮点

1. **异步架构**：FastAPI + 异步 SQLAlchemy，高性能处理
2. **AI 集成**：深度整合 DeepSeek/OpenAI 服务
3. **流式响应**：SSE 实时评估结果
4. **完整的认证体系**：JWT + 权限控制
5. **容器化部署**：快速扩展和部署
6. **模块化设计**：代码结构清晰，易于维护

---

*文档生成时间: 2026-04-20*
