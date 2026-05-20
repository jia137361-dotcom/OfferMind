import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.job_template import JobTemplate
from app.exceptions.http_exceptions import NotFoundError

logger = logging.getLogger(__name__)


class JobTemplateService:
    """岗位模板管理服务"""

    @staticmethod
    async def create_template(
        db: AsyncSession,
        title: str,
        description: str = None,
        required_skills: list = None,
        preferred_skills: list = None,
        responsibilities: list = None,
        question_categories: list = None,
        difficulty_level: str = "medium"
    ) -> JobTemplate:
        template = JobTemplate(
            title=title,
            description=description,
            required_skills=required_skills or [],
            preferred_skills=preferred_skills or [],
            responsibilities=responsibilities or [],
            question_categories=question_categories or [],
            difficulty_level=difficulty_level
        )
        db.add(template)
        await db.commit()
        await db.refresh(template)
        return template

    @staticmethod
    async def get_template(db: AsyncSession, template_id: int) -> dict:
        template = await db.get(JobTemplate, template_id)
        if not template:
            raise NotFoundError(message="岗位模板不存在")
        return JobTemplateService._to_dict(template)

    @staticmethod
    async def list_templates(
        db: AsyncSession,
        is_active: Optional[bool] = None,
        page: int = 1,
        per_page: int = 20
    ) -> dict:
        conditions = []
        if is_active is not None:
            conditions.append(JobTemplate.is_active == is_active)

        query = select(JobTemplate).where(*conditions).order_by(JobTemplate.id.desc())
        count_query = select(func.count()).select_from(JobTemplate).where(*conditions)

        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        result = await db.execute(query)
        templates = result.scalars().all()
        total = await db.scalar(count_query)

        return {
            "total": total or 0,
            "page": page,
            "per_page": per_page,
            "items": [JobTemplateService._to_dict(t) for t in templates]
        }

    @staticmethod
    async def get_active_templates(db: AsyncSession) -> list[dict]:
        """获取所有启用的岗位模板（供 Agent 和前端使用）"""
        query = select(JobTemplate).where(
            JobTemplate.is_active == True
        ).order_by(JobTemplate.title)
        result = await db.execute(query)
        templates = result.scalars().all()
        return [JobTemplateService._to_dict(t) for t in templates]

    @staticmethod
    async def update_template(
        db: AsyncSession,
        template_id: int,
        **kwargs
    ) -> dict:
        template = await db.get(JobTemplate, template_id)
        if not template:
            raise NotFoundError(message="岗位模板不存在")

        for key, value in kwargs.items():
            if hasattr(template, key):
                setattr(template, key, value)

        await db.commit()
        await db.refresh(template)
        return JobTemplateService._to_dict(template)

    @staticmethod
    async def delete_template(db: AsyncSession, template_id: int) -> None:
        template = await db.get(JobTemplate, template_id)
        if not template:
            raise NotFoundError(message="岗位模板不存在")
        await db.delete(template)
        await db.commit()

    @staticmethod
    def _to_dict(t: JobTemplate) -> dict:
        return {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "required_skills": t.required_skills,
            "preferred_skills": t.preferred_skills,
            "responsibilities": t.responsibilities,
            "question_categories": t.question_categories,
            "difficulty_level": t.difficulty_level,
            "is_active": t.is_active,
            "created_at": t.created_at.isoformat() if t.created_at else None
        }
