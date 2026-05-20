from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.client.deps import get_current_user
from app.models.user import User
from app.schemas.response import ApiResponse
from app.services.backoffice.job_template_service import JobTemplateService

router = APIRouter()


@router.get("")
async def list_active_templates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取所有可用的岗位模板"""
    templates = await JobTemplateService.get_active_templates(db)
    return ApiResponse.success(data={"items": templates, "total": len(templates)})
