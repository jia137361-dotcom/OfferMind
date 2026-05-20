from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from app.db.session import get_db
from app.api.backoffice.deps import get_current_admin
from app.models.admin import Admin
from app.schemas.response import ApiResponse
from app.services.client.question_bank_service import QuestionBankService

router = APIRouter()


class CreateQuestionRequest(BaseModel):
    content: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    difficulty: str = Field(default="medium")
    tags: list[str] = Field(default_factory=list)
    reference_answer: str = Field(default="")
    key_points: list[str] = Field(default_factory=list)
    source: str = Field(default="manual")


class UpdateQuestionRequest(BaseModel):
    content: str | None = None
    category: str | None = None
    difficulty: str | None = None
    tags: list[str] | None = None
    reference_answer: str | None = None
    key_points: list[str] | None = None
    is_active: bool | None = None


class SearchQuestionsRequest(BaseModel):
    query_text: str = Field(..., min_length=1)
    category: str | None = None
    difficulty: str | None = None
    top_k: int = Field(default=5, ge=1, le=50)


@router.get("")
async def list_questions(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    category: str | None = None,
    difficulty: str | None = None,
    is_active: bool | None = None,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """获取题目列表"""
    result = await QuestionBankService.list_questions(
        db, category=category, difficulty=difficulty,
        is_active=is_active, page=page, per_page=per_page
    )
    return ApiResponse.success(data=result)


@router.post("")
async def create_question(
    req: CreateQuestionRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """创建题目（自动生成 embedding）"""
    question = await QuestionBankService.add_question(
        db,
        content=req.content,
        category=req.category,
        difficulty=req.difficulty,
        tags=req.tags,
        reference_answer=req.reference_answer,
        key_points=req.key_points,
        source=req.source
    )
    return ApiResponse.success(data=QuestionBankService._to_dict(question))


@router.get("/{question_id}")
async def get_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """获取题目详情"""
    result = await QuestionBankService.get_question(db, question_id)
    return ApiResponse.success(data=result)


@router.put("/{question_id}")
async def update_question(
    question_id: int,
    req: UpdateQuestionRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """更新题目"""
    update_data = {k: v for k, v in req.model_dump().items() if v is not None}
    result = await QuestionBankService.update_question(db, question_id, **update_data)
    return ApiResponse.success(data=result)


@router.delete("/{question_id}")
async def delete_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """删除题目"""
    await QuestionBankService.delete_question(db, question_id)
    return ApiResponse.success(data={"message": "题目已删除"})


@router.post("/search")
async def search_questions(
    req: SearchQuestionsRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """语义搜索题目"""
    results = await QuestionBankService.search_similar(
        db,
        query_text=req.query_text,
        category=req.category,
        difficulty=req.difficulty,
        top_k=req.top_k
    )
    return ApiResponse.success(data={"items": results, "total": len(results)})


@router.post("/seed")
async def seed_questions(
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """导入默认题库"""
    result = await QuestionBankService.seed_default_questions(db)
    return ApiResponse.success(data=result)
