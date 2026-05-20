from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from app.db.session import get_db
from app.api.backoffice.deps import get_current_admin
from app.models.admin import Admin
from app.schemas.response import ApiResponse
from app.services.backoffice.job_template_service import JobTemplateService

router = APIRouter()


class CreateJobTemplateRequest(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(default="")
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    question_categories: list[str] = Field(default_factory=list)
    difficulty_level: str = Field(default="medium")


class UpdateJobTemplateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    required_skills: list[str] | None = None
    preferred_skills: list[str] | None = None
    responsibilities: list[str] | None = None
    question_categories: list[str] | None = None
    difficulty_level: str | None = None
    is_active: bool | None = None


@router.get("")
async def list_templates(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    is_active: bool | None = None,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """获取岗位模板列表"""
    result = await JobTemplateService.list_templates(
        db, is_active=is_active, page=page, per_page=per_page
    )
    return ApiResponse.success(data=result)


@router.post("")
async def create_template(
    req: CreateJobTemplateRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """创建岗位模板"""
    template = await JobTemplateService.create_template(
        db,
        title=req.title,
        description=req.description,
        required_skills=req.required_skills,
        preferred_skills=req.preferred_skills,
        responsibilities=req.responsibilities,
        question_categories=req.question_categories,
        difficulty_level=req.difficulty_level
    )
    return ApiResponse.success(data=JobTemplateService._to_dict(template))


@router.get("/{template_id}")
async def get_template(
    template_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """获取岗位模板详情"""
    result = await JobTemplateService.get_template(db, template_id)
    return ApiResponse.success(data=result)


@router.put("/{template_id}")
async def update_template(
    template_id: int,
    req: UpdateJobTemplateRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """更新岗位模板"""
    update_data = {k: v for k, v in req.model_dump().items() if v is not None}
    result = await JobTemplateService.update_template(db, template_id, **update_data)
    return ApiResponse.success(data=result)


@router.delete("/{template_id}")
async def delete_template(
    template_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """删除岗位模板"""
    await JobTemplateService.delete_template(db, template_id)
    return ApiResponse.success(data={"message": "岗位模板已删除"})
