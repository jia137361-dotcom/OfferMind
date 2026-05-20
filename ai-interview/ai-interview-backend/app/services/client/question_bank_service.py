import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, delete as sql_delete
from app.models.question import Question
from app.services.client.embedding_service import EmbeddingService
from app.exceptions.http_exceptions import NotFoundError

logger = logging.getLogger(__name__)

DEFAULT_QUESTIONS = [
    {
        "content": "请做一个简短的自我介绍，包括你的技术背景和项目经验。",
        "category": "self-intro",
        "difficulty": "easy",
        "tags": ["自我介绍", "通用"],
        "reference_answer": "候选人应清晰介绍姓名、技术栈、核心项目经验、职业目标，时长控制在1-2分钟。",
        "key_points": ["表达流畅", "技术栈明确", "项目经验突出", "时间控制", "逻辑清晰"],
        "source": "seed"
    },
    {
        "content": "请介绍你简历中最有挑战性的项目，你遇到了什么技术难点，是如何解决的？",
        "category": "project",
        "difficulty": "medium",
        "tags": ["项目经验", "问题解决"],
        "reference_answer": "应描述项目背景、核心技术选型、遇到的具体难点（如性能瓶颈、架构设计）、采取的解决方案和最终效果（最好有数据支撑）。",
        "key_points": ["项目复杂度", "技术难点识别", "解决思路", "方案落地", "结果数据"],
        "source": "seed"
    },
    {
        "content": "请解释 HTTP 和 HTTPS 的区别，以及 HTTPS 的工作原理。",
        "category": "technical",
        "difficulty": "easy",
        "tags": ["网络", "HTTP", "安全"],
        "reference_answer": "HTTP是明文传输，HTTPS通过SSL/TLS加密。HTTPS工作流程：TCP握手→TLS握手(证书验证、密钥交换)→对称加密通信。",
        "key_points": ["加密理解", "证书机制", "握手流程", "安全风险认知"],
        "source": "seed"
    },
    {
        "content": "请解释数据库索引的原理，什么情况下索引会失效？",
        "category": "technical",
        "difficulty": "medium",
        "tags": ["数据库", "索引", "性能优化"],
        "reference_answer": "索引基于B+树等数据结构加速查询。失效场景：LIKE前置通配、OR条件不统一、索引列上函数运算、隐式类型转换、联合索引不满足最左前缀。",
        "key_points": ["B+树原理", "失效场景列举", "执行计划分析", "实际优化经验"],
        "source": "seed"
    },
    {
        "content": "请解释 Python 中的 GIL（全局解释器锁），以及它对多线程程序的影响。",
        "category": "technical",
        "difficulty": "medium",
        "tags": ["Python", "并发", "GIL"],
        "reference_answer": "GIL是CPython的互斥锁，保证同一时刻只有一个线程执行Python字节码。CPU密集型任务受限于GIL，应使用多进程；IO密集型可用多线程或asyncio。",
        "key_points": ["GIL定义准确", "CPU密集vsIO密集", "多进程替代方案", "asyncio适用场景"],
        "source": "seed"
    },
    {
        "content": "请解释 Redis 的持久化机制 RDB 和 AOF 的区别及适用场景。",
        "category": "technical",
        "difficulty": "medium",
        "tags": ["Redis", "缓存", "持久化"],
        "reference_answer": "RDB是快照方式定时全量备份，AOF记录每次写操作日志。RDB恢复快但可能丢数据，AOF数据安全性高但文件更大。生产环境建议两者结合使用。",
        "key_points": ["RDB原理", "AOF原理", "优缺点对比", "混合持久化", "实际配置经验"],
        "source": "seed"
    },
    {
        "content": "请设计一个短链接系统（类似 TinyURL），需要考虑高并发和大流量。",
        "category": "system-design",
        "difficulty": "hard",
        "tags": ["系统设计", "分布式", "高并发"],
        "reference_answer": "核心流程：长URL→hash/发号器→短码→存储。需考虑：分布式发号器(雪花算法)、Base62编码、缓存层(Redis)、数据库分片、302重定向、过期策略、访问统计。",
        "key_points": ["需求分析", "发号器设计", "存储方案", "缓存策略", "扩展性考虑", "并发处理"],
        "source": "seed"
    },
    {
        "content": "请写一个函数，判断一个字符串是否是有效的括号匹配。例如 \"()[]{}\" 返回 True，\"([)]\" 返回 False。",
        "category": "coding",
        "difficulty": "easy",
        "tags": ["算法", "栈", "编码"],
        "reference_answer": "使用栈数据结构：遍历字符，左括号入栈，右括号检查栈顶是否匹配。最后检查栈是否为空。时间复杂度O(n)，空间复杂度O(n)。",
        "key_points": ["算法思路正确", "边界情况处理", "时间/空间复杂度", "代码简洁"],
        "source": "seed"
    },
    {
        "content": "请解释微服务架构的优缺点，以及你们项目中是如何进行服务拆分的。",
        "category": "system-design",
        "difficulty": "hard",
        "tags": ["微服务", "架构", "分布式"],
        "reference_answer": "优点：独立部署、技术栈灵活、故障隔离、团队自治。缺点：分布式复杂性、网络延迟、数据一致性、运维成本高。拆分原则：按业务域拆分、高内聚低耦合、数据独立。",
        "key_points": ["优缺点全面", "拆分原则合理", "实际经验", "技术选型理解"],
        "source": "seed"
    },
    {
        "content": "请描述你在项目中如何进行性能优化，解决了一个具体的性能瓶颈问题。",
        "category": "project",
        "difficulty": "hard",
        "tags": ["性能优化", "问题定位", "实战"],
        "reference_answer": "应描述完整优化流程：监控发现→profiling定位瓶颈→分析原因→制定方案→实施验证→效果对比。具体手段：缓存、索引优化、SQL优化、异步化、连接池调优等。",
        "key_points": ["优化流程完整", "瓶颈定位方法", "方案合理性", "效果量化", "总结反思"],
        "source": "seed"
    },
]


class QuestionBankService:
    """题库管理服务 — CRUD + RAG 语义检索"""

    @staticmethod
    async def add_question(
        db: AsyncSession,
        content: str,
        category: str,
        difficulty: str = "medium",
        tags: list = None,
        reference_answer: str = None,
        key_points: list = None,
        source: str = "manual"
    ) -> Question:
        embedding = await EmbeddingService.embed_text(content)
        question = Question(
            content=content,
            category=category,
            difficulty=difficulty,
            tags=tags or [],
            reference_answer=reference_answer,
            key_points=key_points or [],
            embedding=embedding,
            source=source
        )
        db.add(question)
        await db.commit()
        await db.refresh(question)
        return question

    @staticmethod
    async def search_similar(
        db: AsyncSession,
        query_text: str,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        top_k: int = 5
    ) -> list[dict]:
        """语义检索：embed 查询文本 → pgvector 余弦相似度搜索"""
        query_embedding = await EmbeddingService.embed_text(query_text)

        conditions = ["q.is_active = true"]
        params = {"embedding": query_embedding, "top_k": top_k}

        if category:
            conditions.append("q.category = :category")
            params["category"] = category
        if difficulty:
            conditions.append("q.difficulty = :difficulty")
            params["difficulty"] = difficulty

        where_clause = " AND ".join(conditions)

        sql = text(f"""
            SELECT q.id, q.content, q.category, q.difficulty, q.tags,
                   q.reference_answer, q.key_points, q.source,
                   1 - (q.embedding <=> :embedding) AS similarity
            FROM questions q
            WHERE {where_clause}
            ORDER BY q.embedding <=> :embedding
            LIMIT :top_k
        """)

        result = await db.execute(sql, params)
        rows = result.fetchall()

        return [
            {
                "id": row.id,
                "content": row.content,
                "category": row.category,
                "difficulty": row.difficulty,
                "tags": row.tags,
                "reference_answer": row.reference_answer,
                "key_points": row.key_points,
                "source": row.source,
                "similarity": round(float(row.similarity), 4)
            }
            for row in rows
        ]

    @staticmethod
    async def get_question(db: AsyncSession, question_id: int) -> dict:
        query = select(Question).where(Question.id == question_id)
        result = await db.execute(query)
        question = result.scalar_one_or_none()
        if not question:
            raise NotFoundError(message="题目不存在")
        return QuestionBankService._to_dict(question)

    @staticmethod
    async def list_questions(
        db: AsyncSession,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        per_page: int = 20
    ) -> dict:
        conditions = []
        if category:
            conditions.append(Question.category == category)
        if difficulty:
            conditions.append(Question.difficulty == difficulty)
        if is_active is not None:
            conditions.append(Question.is_active == is_active)

        query = select(Question).where(*conditions).order_by(Question.id.desc())
        count_query = select(Question).where(*conditions)

        # 简单分页（不使用 paginator 以保持轻量）
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        result = await db.execute(query)
        questions = result.scalars().all()

        count_result = await db.execute(count_query)
        total = len(count_result.scalars().all())

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "items": [QuestionBankService._to_dict(q) for q in questions]
        }

    @staticmethod
    async def update_question(
        db: AsyncSession,
        question_id: int,
        **kwargs
    ) -> dict:
        query = select(Question).where(Question.id == question_id)
        result = await db.execute(query)
        question = result.scalar_one_or_none()
        if not question:
            raise NotFoundError(message="题目不存在")

        # 如果更新了 content，重新生成 embedding
        if "content" in kwargs and kwargs["content"] != question.content:
            question.embedding = await EmbeddingService.embed_text(kwargs["content"])

        for key, value in kwargs.items():
            if hasattr(question, key):
                setattr(question, key, value)

        await db.commit()
        await db.refresh(question)
        return QuestionBankService._to_dict(question)

    @staticmethod
    async def delete_question(db: AsyncSession, question_id: int) -> None:
        query = select(Question).where(Question.id == question_id)
        result = await db.execute(query)
        question = result.scalar_one_or_none()
        if not question:
            raise NotFoundError(message="题目不存在")
        await db.delete(question)
        await db.commit()

    @staticmethod
    async def seed_default_questions(db: AsyncSession) -> dict:
        """导入默认题库，跳过已存在的相似题目"""
        inserted = 0
        skipped = 0
        for item in DEFAULT_QUESTIONS:
            # 检查是否已存在相同 content 的题目
            existing = await db.execute(
                select(Question).where(Question.content == item["content"])
            )
            if existing.scalar_one_or_none():
                skipped += 1
                continue

            await QuestionBankService.add_question(db, **item)
            inserted += 1

        return {"inserted": inserted, "skipped": skipped, "total": len(DEFAULT_QUESTIONS)}

    @staticmethod
    def _to_dict(q: Question) -> dict:
        return {
            "id": q.id,
            "content": q.content,
            "category": q.category,
            "difficulty": q.difficulty,
            "tags": q.tags,
            "reference_answer": q.reference_answer,
            "key_points": q.key_points,
            "source": q.source,
            "is_active": q.is_active,
            "created_at": q.created_at.isoformat() if q.created_at else None
        }
