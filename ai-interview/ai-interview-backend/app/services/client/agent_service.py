import json
import logging
import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.resume import Resume
from app.models.job_template import JobTemplate
from app.services.client.interview_service import InterviewService
from app.services.client.ai_service import AIService

logger = logging.getLogger(__name__)


class InterviewAgentService:
    """Agent 驱动的面试设置 — 直接从数据库读简历，一次 AI 调用完成岗位匹配"""

    def __init__(self, db: AsyncSession, user_id: int):
        self.db = db
        self.user_id = user_id

    async def run_setup(self, resume_id: int) -> dict:
        try:
            # 从数据库读取已解析的简历
            query = select(Resume).where(Resume.id == resume_id, Resume.user_id == self.user_id)
            result = await self.db.execute(query)
            resume = result.scalar_one_or_none()
            if not resume or resume.status != "completed":
                return {"success": False, "output": "简历不存在或未解析完成", "interview_id": None}

            resume_data = json.loads(resume.parsed_content or "{}")
            analysis_data = json.loads(resume.analysis or "{}")

            # 获取活跃岗位模板
            query = select(JobTemplate).where(JobTemplate.is_active == True)
            result = await self.db.execute(query)
            templates = result.scalars().all()
            if not templates:
                return {"success": False, "output": "没有可用岗位模板", "interview_id": None}

            templates_info = [
                {"id": t.id, "title": t.title, "description": t.description,
                 "required_skills": t.required_skills, "preferred_skills": t.preferred_skills,
                 "difficulty_level": t.difficulty_level}
                for t in templates
            ]

            # 一次 AI 调用完成画像分析 + 岗位匹配
            match_prompt = f"""请分析候选人信息并匹配最合适的岗位。

候选人简历摘要：{json.dumps(resume_data, ensure_ascii=False)[:800]}
简历分析：优势 {json.dumps(analysis_data.get('strengths', []), ensure_ascii=False)}
技能匹配：{json.dumps(analysis_data.get('keyword_match', []), ensure_ascii=False)}
缺少技能：{json.dumps(analysis_data.get('missing_keywords', []), ensure_ascii=False)}

可选岗位模板：{json.dumps(templates_info, ensure_ascii=False)}

请直接选择最匹配的岗位，返回纯JSON格式（不要markdown）：
{{"selected_template_id": 1, "title": "岗位名", "fit_score": 85, "reason": "理由", "difficulty": "medium"}}"""

            messages = [{"role": "user", "content": match_prompt}]
            match_result_str = await AIService._chat(messages, temperature=0.3)
            match_data = self._parse_json(match_result_str)

            # 取最佳匹配
            template_id = match_data.get("selected_template_id")
            title = match_data.get("title", templates[0].title)
            difficulty = match_data.get("difficulty", "medium")

            if not template_id:
                template_id = templates[0].id

            # 直接创建面试
            interview_data = await InterviewService.start_interview(
                db=self.db, user_id=self.user_id, resume_id=resume_id,
                target_position=title, difficulty=difficulty, total_questions=5
            )

            return {
                "success": True,
                "output": f"已匹配岗位「{title}」并创建面试",
                "interview_id": interview_data["interview_id"],
                "match": match_data
            }
        except Exception as e:
            logger.error(f"Agent 执行失败: {e}")
            return {"success": False, "output": str(e), "interview_id": None}

    @staticmethod
    def _parse_json(content: str) -> dict:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass
        m = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                pass
        m = re.search(r'\{[\s\S]*\}', content)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
        return {}
