# OfferMind 职引 — 部署文档

## 环境要求

| 组件 | 最低版本 | 说明 |
|------|---------|------|
| Python | 3.12+ | 异步特性需要 |
| Node.js | 18+ | 前端构建 |
| PostgreSQL | 16 | pgvector 扩展支持 |
| Redis | 7 | Celery 消息队列 + 会话缓存 |
| Docker | 24+ | 可选，容器化部署 |

## 一、裸机部署

### 1.1 安装 PostgreSQL 16 + pgvector

**Ubuntu/Debian:**
```bash
sudo apt install postgresql-16 postgresql-16-pgvector
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

**macOS:**
```bash
brew install postgresql@16
brew install pgvector
```

**Windows:**
下载安装 [PostgreSQL 16](https://www.postgresql.org/download/windows/)，然后手动安装 pgvector 扩展：
```sql
CREATE EXTENSION vector;
```

### 1.2 创建数据库
```sql
CREATE USER demo WITH PASSWORD 'demo123';
CREATE DATABASE ai_interview OWNER demo;
\c ai_interview
CREATE EXTENSION IF NOT EXISTS vector;
```

### 1.3 安装 Redis
```bash
# Ubuntu
sudo apt install redis-server

# macOS
brew install redis

# Windows
# 使用 WSL 或下载 Redis for Windows
```

### 1.4 配置环境变量

复制 `.env.example` 为 `.env`：
```bash
cd ai-interview-backend
cp .env.example .env
```

编辑 `.env`，修改以下配置：
```env
# 数据库（填写你的实际地址）
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=demo
POSTGRES_PASSWORD=demo123
POSTGRES_DB=ai_interview

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# DeepSeek LLM（必填）
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

# DashScope Embedding（必填，RAG 题库需要）
DASHSCOPE_API_KEY=sk-xxx
DASHSCOPE_EMBEDDING_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_EMBEDDING_MODEL=text-embedding-v4
```

### 1.5 安装 Python 依赖
```bash
cd ai-interview-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install langchain langchain-openai pgvector
```

### 1.6 数据库迁移
```bash
cd ai-interview-backend
alembic upgrade head
```

### 1.7 启动后端
```bash
# 开发模式
python main.py
# 或使用 uvicorn
uvicorn app.route:create_app --host 0.0.0.0 --port 8006 --reload

# 生产模式（多 worker）
uvicorn app.route:create_app --host 0.0.0.0 --port 8006 --workers 4
```

### 1.8 启动 Celery Worker
```bash
celery -A app.core.celery_app worker --loglevel=info
```

### 1.9 安装和启动前端
```bash
# 用户端
cd ai-interview-frontend
npm install
npm run build   # 生产构建
# 开发模式
npm run dev     # http://localhost:3000

# 管理后台
cd ai-interview-admin
npm install
npm run build
npm run dev     # http://localhost:3001
```

### 1.10 配置 Nginx（生产环境）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    root /path/to/ai-interview-frontend/dist;
    index index.html;

    # API 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8006;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 上传文件
    location /uploads/ {
        proxy_pass http://127.0.0.1:8006;
    }

    # 前端 SPA
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

---

## 二、Docker Compose 部署（推荐）

### 2.1 配置环境变量
```bash
cd ai-interview-backend
cp .env.example .env
# 编辑 .env，Docker 环境下数据库地址用服务名：
# POSTGRES_HOST=postgres
# REDIS_HOST=redis
```

### 2.2 启动所有服务
```bash
docker compose up -d --build
```

启动的服务：
| 服务 | 容器名 | 端口 |
|------|--------|------|
| FastAPI | ai-interview-app | 8006 |
| Celery Worker | ai-interview-celery-worker | - |
| Celery Beat | ai-interview-celery-beat | - |
| PostgreSQL 16 | ai-interview-postgres | 5434 |
| Redis 7 | ai-interview-redis | 6382 |
| Nginx | ai-interview-nginx | 8080, 8443 |
| Flower (可选) | ai-interview-flower | 5555 |

### 2.3 运行数据库迁移
```bash
docker exec ai-interview-app alembic upgrade head
```

### 2.4 初始化管理员
```bash
docker exec ai-interview-app python -c "
import asyncio; from app.db.session import get_db; from app.models.admin import Admin
async def seed():
    db = await anext(get_db())
    admin = Admin(email='admin@ai-interview.com', role='superadmin', first_name='Admin', is_active=True)
    admin.password = Admin.get_password_hash('admin123')
    db.add(admin); await db.commit()
asyncio.run(seed())
"
```

### 2.5 启动 Flower 监控（可选）
```bash
docker compose --profile monitoring up -d
# 访问 http://localhost:5555
```

---

## 三、生产环境检查清单

- [ ] `.env` 中 `ENV=production`
- [ ] 修改 `SECRET_KEY` 为随机字符串（`openssl rand -hex 32`）
- [ ] 修改默认管理员密码
- [ ] 配置真实的 SMTP 邮件服务（Brevo / AWS SES）
- [ ] 配置 AWS S3 存储（用于生产环境文件上传）
- [ ] 配置 HTTPS 证书（Let's Encrypt / Certbot）
- [ ] 设置 Redis 密码
- [ ] 配置 PostgreSQL 连接池参数（`.env` 中调整）
- [ ] 设置防火墙规则（仅开放 80/443 端口）
- [ ] 配置日志级别为 WARNING
- [ ] 关闭 Swagger 文档（生产环境 `openapi_url=None`）

---

## 四、CI/CD（GitHub Actions）

项目包含 3 个 GitHub Actions 工作流：

| 工作流 | 触发条件 | 说明 |
|--------|----------|------|
| `quick-check.yml` | PR | 语法检查、代码格式、安全扫描 |
| `preview-deploy.yml` | 手动触发 | 预览环境部署 |
| `production-deploy.yml` | 推送到 main | 生产部署（含备份和回滚） |

### 配置 Secrets
在 GitHub Settings → Secrets and variables → Actions 中添加：
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `SSH_HOST` / `SSH_USERNAME` / `SSH_PRIVATE_KEY`

---

## 五、常见问题

### Q: 数据库连接失败
检查 `.env` 中 `POSTGRES_HOST`、`POSTGRES_PORT` 是否正确。Docker 部署时 `POSTGRES_HOST=postgres`（服务名）。

### Q: pgvector 扩展不存在
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Q: DeepSeek API 调用失败
检查 `DEEPSEEK_BASE_URL` 是否正确。应该为 `https://api.deepseek.com`（不要加 `/v1`）。

### Q: 前端请求 500 错误
检查 `vite.config.js` 中代理地址是否为 `http://localhost:8006`。

### Q: Celery Worker 未启动
```bash
celery -A app.core.celery_app worker --loglevel=info
```

---

## 六、服务端口总览

| 服务 | 开发端口 | Docker 端口 |
|------|---------|------------|
| 后端 API | 8006 | 8006 |
| 用户端前端 | 3000 | - |
| 管理后台 | 3001 | - |
| PostgreSQL | 5434 | 5434 |
| Redis | 6382 | 6382 |
| Nginx | - | 8080 / 8443 |
| Flower | 5555 | 5555 |
