# OfferMind 职引 — AI 模拟面试平台

> AI Interview Coach — 基于 RAG 与 Agent 的智能模拟面试系统

面向求职场景设计的 AI 模拟面试平台，围绕「简历解析 → 岗位匹配 → RAG 出题 → AI 评分 → 面试报告」构建完整闭环，帮助候选人高效备战技术面试。

---

## 技术栈

### 后端
| 技术 | 用途 |
|------|------|
| **FastAPI** | 异步 Web 框架，RESTful API |
| **PostgreSQL 16 + pgvector** | 关系型数据库 + 向量存储与语义搜索 |
| **Redis 7** | 缓存、会话管理、Celery 消息队列 |
| **Celery** | 异步任务调度（邮件发送、定时任务） |
| **SQLAlchemy 2.0 (Async)** | 异步 ORM + Alembic 数据库迁移 |
| **DeepSeek API** | LLM：简历解析、画像提取、出题、评分、报告生成 |
| **DashScope Embedding (text-embedding-v4)** | 文本向量化，题库 RAG 语义检索 |
| **LangChain 1.3 + LangChain-OpenAI** | Tool Calling Agent，岗位匹配自动化 |
| **JWT (python-jose)** | 双 Token 认证（Access + Refresh） |
| **pdfplumber** | PDF 简历文本提取 |

### 前端
| 技术 | 用途 |
|------|------|
| **Vue 3 (Composition API)** | 渐进式前端框架 |
| **Vue Router 4** | 单页应用路由 |
| **Pinia** | 状态管理 |
| **Axios** | HTTP 请求 + 拦截器 |
| **Vite 5** | 构建工具 + HMR 热更新 |

### DevOps
| 技术 | 用途 |
|------|------|
| **Docker Compose** | 多服务编排（API / Celery / PostgreSQL / Redis / Nginx） |
| **Nginx** | 反向代理 + SSL 终端 |
| **GitHub Actions** | CI/CD（语法检查、构建、部署） |

---

## 项目架构

```
OfferMind/
├── ai-interview-backend/          # FastAPI 后端
│   ├── app/
│   │   ├── api/client/v1/         # 用户端 API（面试、简历、认证）
│   │   ├── api/backoffice/v1/     # 管理后台 API（题库、用户、面试管理）
│   │   ├── core/                  # 配置、JWT、日志、Celery
│   │   ├── db/                    # 数据库引擎、会话管理
│   │   ├── models/                # ORM 模型（User, Resume, Interview, Question, JobTemplate...）
│   │   ├── route/                 # 路由注册中心
│   │   ├── schemas/               # Pydantic 请求/响应模型
│   │   ├── services/client/       # 核心业务：AI 服务、面试引擎、Agent、RAG 题库
│   │   └── services/backoffice/   # 后台管理服务
│   ├── migrations/                # Alembic 数据库迁移
│   ├── resources/emails/          # 邮件模板
│   └── docker-compose.yml         # Docker 编排
├── ai-interview-frontend/         # 用户端 Vue 3
│   └── src/views/                 # 登录、仪表盘、简历上传、面试、报告
└── ai-interview-admin/            # 管理后台 Vue 3
    └── src/views/                 # 概览、用户管理、面试记录
```

---

## 核心功能

### 1. 简历智能解析
- 上传 PDF 简历 → pdfplumber 提取文本 → DeepSeek 结构化解析 + 质量分析
- 输出：姓名、学历、技能列表、项目经历、优劣势、匹配度评分、改进建议

### 2. RAG 增强出题（pgvector + DashScope Embedding）
- 题库题目通过 DashScope `text-embedding-v4` 向量化存入 pgvector
- 面试出题时自动语义检索相关题目作为上下文注入 Prompt
- 支持按分类、难度筛选，HNSW 索引加速检索

### 3. LangChain Agent 岗位匹配
- 4 个 Tool：`read_resume` → `build_candidate_profile` → `match_job_templates` → `start_specialized_interview`
- DeepSeek 驱动 Agent 自动执行简历读取 → 画像构建 → 岗位匹配 → 面试启动
- 管理员可自定义岗位模板（技能要求、职责、题目分类）

### 4. 参考答案注入评分
- 每道面试题自动生成 `reference_answer`（参考答案）和 `key_points`（关键得分点）
- 评分时注入 Prompt，LLM 对照参考答案逐项评分
- 提升评分稳定性和可解释性

### 5. 面试报告
- 综合所有问答生成评估报告：总分、优劣势、改进建议、录用推荐
- 每题独立评分 + 反馈

---

## 运行流程

```
用户注册/登录
    ↓
上传 PDF 简历 → AI 解析简历 + 质量分析
    ↓
开始面试（3 种方式）:
  · 手动：选择岗位、难度、题数
  · Agent：自动画像 → 岗位匹配 → 启动专项面试
  · 继续：进行中的面试直接继续
    ↓
逐题作答（SSE 流式评分）
    ↓
面试完成 → 生成综合评估报告
```

---

## 快速开始

### 环境要求
- Python 3.12+
- Node.js 18+
- PostgreSQL 16 + pgvector 扩展
- Redis 7

### 1. 克隆项目
```bash
git clone https://github.com/jia137361-dotcom/OfferMind.git
cd OfferMind/ai-interview/ai-interview-backend
```

### 2. 配置环境变量
编辑 `.env` 文件，填入你的 API Key：
```env
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

DASHSCOPE_API_KEY=sk-xxx
DASHSCOPE_EMBEDDING_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_EMBEDDING_MODEL=text-embedding-v4
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
pip install langchain langchain-openai pgvector

# 前端
cd ../ai-interview-frontend && npm install
cd ../ai-interview-admin && npm install
```

### 4. 数据库迁移
```bash
cd ai-interview-backend
alembic upgrade head
```

### 5. 启动服务
```bash
# 后端
cd ai-interview-backend
python main.py    # http://localhost:8006

# 前端
cd ai-interview-frontend
npm run dev       # http://localhost:3000

# 管理后台
cd ai-interview-admin
npm run dev       # http://localhost:3001
```

### 6. 初始化数据
```bash
# 创建管理员
python -c "
import asyncio; from app.db.session import get_db; from app.models.admin import Admin
async def seed():
    db = await anext(get_db())
    admin = Admin(email='admin@ai-interview.com', role='superadmin', first_name='Admin', is_active=True)
    admin.password = Admin.get_password_hash('admin123')
    db.add(admin); await db.commit()
asyncio.run(seed())
"

# 导入题库种子数据（需先登录管理员获取 Token）
curl -X POST http://localhost:8006/api/v1/backoffice/questions/seed \
  -H "Authorization: Bearer <admin_token>"
```

### Docker 部署
```bash
docker compose up -d --build
```
启动后访问：
- 用户端: `http://localhost:3000`
- 管理后台: `http://localhost:3001`
- API 文档: `http://localhost:8006/client/docs`

---

## 默认账号

| 角色 | 邮箱 | 密码 |
|------|------|------|
| 管理员 | admin@ai-interview.com | admin123 |

> 用户通过注册页面自行注册，邮箱验证在开发环境下可跳过。

---

## API 文档

| 文档 | 地址 |
|------|------|
| 用户端 Swagger | `http://localhost:8006/client/docs` |
| 管理后台 Swagger | `http://localhost:8006/backoffice/docs` |

---

## 项目特色

- **RAG 增强出题**：pgvector + DashScope Embedding 语义检索，题目与岗位精准匹配
- **Agent 自动化**：LangChain Tool Calling 串联简历分析→画像→岗位匹配→面试启动
- **可解释评分**：参考答案 + 关键得分点注入 Prompt，评分有据可依
- **SSE 流式反馈**：答题后实时流式输出 AI 点评
- **双前端架构**：用户端（面试）+ 管理后台（题库/岗位模板管理）
- **插件化题库**：支持手动添加 + 语义搜索 + 一键种子导入

---

## License

MIT
