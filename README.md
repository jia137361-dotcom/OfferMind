# AI Interview System

一个基于 AI 的智能面试系统，帮助求职者提升面试技能，为企业提供人才评估工具。

## 项目特点

- 🎯 **智能面试**：基于简历生成个性化面试题目
- 🤖 **AI 评估**：实时评估面试表现
- 📊 **详细报告**：生成完整的面试分析报告
- 🔐 **安全认证**：完善的用户认证和权限管理
- 📱 **响应式设计**：支持多种设备访问

## 技术栈

### 前端
- **框架**：Vue 3 + Vite
- **路由**：Vue Router 4
- **状态管理**：Pinia
- **HTTP 客户端**：Axios

### 后端
- **框架**：FastAPI（异步为主）
- **数据库**：PostgreSQL + SQLAlchemy 2.0 Async
- **缓存/队列**：Redis
- **后台任务**：Celery
- **身份验证**：JWT
- **AI 集成**：DeepSeek API

### 部署
- **容器化**：Docker + Docker Compose
- **反向代理**：Nginx

## 项目结构

```
ai-interview/
├── ai-interview-admin/     # 后台管理系统
├── ai-interview-backend/   # 后端 API 服务
├── ai-interview-frontend/  # 用户前端界面
└── README.md
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- Docker（推荐）

### 使用 Docker 部署

```bash
# 进入后端目录
cd ai-interview-backend

# 启动所有服务
docker-compose up -d

# 初始化数据库
docker-compose exec api python scripts/create_first_admin.py
```

### 手动运行

#### 后端服务

```bash
cd ai-interview-backend

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
cp .env.example .env
# 编辑 .env 文件配置数据库等信息

# 启动服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 前端服务

```bash
cd ai-interview-frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## API 文档

启动服务后，访问以下地址查看 API 文档：

- **客户端 API**：http://localhost:8000/docs
- **后台管理 API**：http://localhost:8000/backoffice/docs

## 功能模块

### 用户端功能
- 用户注册/登录
- 简历上传与解析
- AI 面试体验
- 面试报告查看
- 个人资料管理

### 后台管理功能
- 用户管理
- 面试记录管理
- 等待列表管理
- 数据统计Dashboard

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DATABASE_URL` | 数据库连接地址 | - |
| `REDIS_URL` | Redis 连接地址 | - |
| `SECRET_KEY` | JWT 密钥 | - |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | - |
| `SMTP_HOST` | SMTP 服务器地址 | - |
| `SMTP_PORT` | SMTP 端口 | 587 |

## 开发指南

### 添加新功能

1. 在 `app/schemas/` 中定义数据模型
2. 在 `app/models/` 中定义数据库模型
3. 在 `app/api/` 中添加路由
4. 在 `app/services/` 中实现业务逻辑

### 代码风格

- 使用 `black` 进行代码格式化
- 使用 `flake8` 进行代码检查
- 使用 `mypy` 进行类型检查

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues：https://github.com/jia137361-dotcom/ai-interview/issues
