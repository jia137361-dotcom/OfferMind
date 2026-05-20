import logging
from openai import AsyncOpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

embedding_client = AsyncOpenAI(
    api_key=settings.DASHSCOPE_API_KEY,
    base_url=settings.DASHSCOPE_EMBEDDING_BASE_URL
)


class EmbeddingService:
    """DashScope Embedding 服务 — 文本向量化"""

    @staticmethod
    async def embed_text(text: str) -> list[float]:
        """单条文本向量化"""
        try:
            response = await embedding_client.embeddings.create(
                model=settings.DASHSCOPE_EMBEDDING_MODEL,
                input=text,
                dimensions=1024
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Embedding API 调用失败: {e}")
            raise

    @staticmethod
    async def embed_batch(texts: list[str]) -> list[list[float]]:
        """批量文本向量化"""
        try:
            response = await embedding_client.embeddings.create(
                model=settings.DASHSCOPE_EMBEDDING_MODEL,
                input=texts,
                dimensions=1024
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Embedding 批量 API 调用失败: {e}")
            raise
