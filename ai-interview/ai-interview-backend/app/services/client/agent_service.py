import json
import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage

from app.core.config import settings
from app.models.resume import Resume
from app.models.job_template import JobTemplate
from app.services.client.interview_service import InterviewService
from app.services.client.ai_service import AIService

logger = logging.getLogger(__name__)


AGENT_SYSTEM_PROMPT = """你是一个专业的AI面试系统助手，负责帮助候选人完成从简历到面试的完整流程。

你的工作流程是：
1. 读取候选人的简历内容
2. 基于简历构建候选人技术画像
3. 将画像与可用的岗位模板进行匹配
4. 自动选择匹配度最高的岗位，直接启动面试

请严格按照以下步骤操作，不要跳过任何一步：
- 首先使用 read_resume 工具读取简历
- 然后使用 build_candidate_profile 工具构建候选人画像
- 接着使用 match_job_templates 工具匹配岗位
- 最后使用 start_specialized_interview 工具，用匹配结果中得分最高的岗位模板直接启动面试

重要：你必须调用 start_specialized_interview 工具，不要只返回匹配结果而不启动面试。用户期望立即开始面试。"""


class InterviewAgentService:
    """LangChain Tool Calling Agent — 岗位匹配与面试启动"""

    def __init__(self, db: AsyncSession, user_id: int):
        self.db = db
        self.user_id = user_id

        self.llm = ChatOpenAI(
            model=settings.DEEPSEEK_MODEL,
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
            temperature=0.3,
            max_tokens=2000
        )

    def _create_tools(self) -> list:
        db = self.db
        user_id = self.user_id

        @tool
        async def read_resume(resume_id: int) -> str:
            """读取指定简历的解析内容。参数 resume_id 为简历 ID。"""
            query = select(Resume).where(
                Resume.id == resume_id,
                Resume.user_id == user_id
            )
            result = await db.execute(query)
            resume = result.scalar_one_or_none()

            if not resume:
                return "错误：简历不存在或不属于当前用户"

            if resume.status != "completed":
                return f"简历状态为 {resume.status}，尚未解析完成"

            parsed = resume.parsed_content or "{}"
            analysis = resume.analysis or "{}"
            target = resume.target_position or "未指定"

            return json.dumps({
                "resume_id": resume.id,
                "target_position": target,
                "parsed_content": json.loads(parsed) if isinstance(parsed, str) else parsed,
                "analysis": json.loads(analysis) if isinstance(analysis, str) else analysis
            }, ensure_ascii=False)

        @tool
        async def build_candidate_profile(resume_text: str) -> str:
            """基于简历内容构建候选人技术画像。
            参数 resume_text 为简历的完整结构化内容（JSON 字符串）。"""
            try:
                profile_prompt = f"""请基于以下简历内容构建候选人技术画像，返回纯JSON格式（不要markdown代码块）：
{{
    "technical_stack": ["技术1", "技术2", ...],
    "experience_level": "初级/中级/高级/资深",
    "years_of_experience": "估算年限",
    "strengths": ["优势1", "优势2", ...],
    "weaknesses": ["不足1", "不足2", ...],
    "education_background": "学历背景简述",
    "suggested_positions": ["建议岗位1", "建议岗位2", ...],
    "summary": "一句话总结候选人画像"
}}

简历内容：
{resume_text}"""
                messages = [{"role": "user", "content": profile_prompt}]
                result = await AIService._chat(messages, temperature=0.3)
                return result
            except Exception as e:
                logger.error(f"构建候选人画像失败: {e}")
                return f"构建画像失败: {str(e)}"

        @tool
        async def match_job_templates(profile_json: str) -> str:
            """将候选人画像与可用岗位模板进行匹配。
            参数 profile_json 为候选人技术画像的 JSON 字符串。"""
            try:
                query = select(JobTemplate).where(JobTemplate.is_active == True)
                result = await db.execute(query)
                templates = result.scalars().all()

                if not templates:
                    return "当前没有可用的岗位模板，请通知管理员添加岗位模板。"

                templates_data = [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "required_skills": t.required_skills,
                        "preferred_skills": t.preferred_skills,
                        "responsibilities": t.responsibilities,
                        "difficulty_level": t.difficulty_level
                    }
                    for t in templates
                ]

                match_prompt = f"""请将候选人画像与以下岗位模板进行匹配，对每个岗位给出匹配度评分（0-100）和匹配理由。

候选人画像：
{profile_json}

岗位模板列表：
{json.dumps(templates_data, ensure_ascii=False)}

返回纯JSON格式（不要markdown代码块）：
{{
    "matches": [
        {{
            "template_id": 1,
            "title": "岗位名称",
            "fit_score": 85,
            "match_reason": "匹配理由...",
            "missing_skills": ["缺失技能1"],
            "interview_suggestion": "面试建议..."
        }}
    ],
    "best_match": {{ "template_id": 1, "title": "...", "fit_score": 85 }},
    "summary": "总体匹配分析"
}}"""
                messages = [{"role": "user", "content": match_prompt}]
                result = await AIService._chat(messages, temperature=0.4)
                return result
            except Exception as e:
                logger.error(f"岗位匹配失败: {e}")
                return f"岗位匹配失败: {str(e)}"

        @tool
        async def start_specialized_interview(
            resume_id: int,
            job_template_id: int,
            difficulty: str = "medium",
            total_questions: int = 5
        ) -> str:
            """启动专项面试。
            参数：
            - resume_id: 简历 ID
            - job_template_id: 岗位模板 ID
            - difficulty: 难度（easy/medium/hard），默认 medium
            - total_questions: 题目数量，默认 5"""
            try:
                template = await db.get(JobTemplate, job_template_id)
                if not template:
                    return "错误：岗位模板不存在"

                interview_data = await InterviewService.start_interview(
                    db=db,
                    user_id=user_id,
                    resume_id=resume_id,
                    target_position=template.title,
                    difficulty=difficulty,
                    total_questions=total_questions
                )
                return json.dumps({
                    "status": "success",
                    "message": f"面试已启动！岗位：{template.title}",
                    "interview_id": interview_data["interview_id"],
                    "first_question": interview_data["first_question"],
                    "total_questions": total_questions,
                    "difficulty": difficulty
                }, ensure_ascii=False)
            except Exception as e:
                logger.error(f"启动面试失败: {e}")
                return f"启动面试失败: {str(e)}"

        return [read_resume, build_candidate_profile, match_job_templates, start_specialized_interview]

    async def run_setup(self, resume_id: int) -> dict:
        """运行 Agent 驱动的面试设置流程 — 优化版：直接从数据库读简历，跳过冗余 AI 调用"""
        try:
            # 1. 直接从数据库读简历（已有解析结果，不再调 AI）
            query = select(Resume).where(
                Resume.id == resume_id,
                Resume.user_id == self.user_id
            )
            result = await self.db.execute(query)
            resume = result.scalar_one_or_none()
            if not resume:
                return {"success": False, "output": "简历不存在", "interview_id": None}
            if resume.status != "completed":
                return {"success": False, "output": f"简历状态: {resume.status}", "interview_id": None}

            resume_data = json.loads(resume.parsed_content or "{}")
            analysis_data = json.loads(resume.analysis or "{}")

            # 2. 获取活跃岗位模板
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

            # 3. 一次 AI 调用完成画像摘要 + 岗位匹配
            match_prompt = f"""请分析候选人信息并匹配最合适的岗位。

候选人简历摘要：
{json.dumps(resume_data, ensure_ascii=False)[:800]}

简历分析结果：
优势：{json.dumps(analysis_data.get('strengths', []), ensure_ascii=False)}
技能：{json.dumps(analysis_data.get('keyword_match', []), ensure_ascii=False)}
缺少技能：{json.dumps(analysis_data.get('missing_keywords', []), ensure_ascii=False)}

可选岗位模板：
{json.dumps(templates_info, ensure_ascii=False)}

请直接选择最匹配的岗位并返回纯JSON（不要markdown代码块）：
{{"selected_template_id": 1, "title": "岗位名", "fit_score": 85, "reason": "简短匹配理由", "difficulty": "medium"}}"""

            messages = [{"role": "user", "content": match_prompt}]
            match_result_str = await AIService._chat(messages, temperature=0.3)
            match_data = self._parse_match_result(match_result_str)

            # 4. 用最佳匹配直接创建面试
            best = match_data.get("selected_template_id")
            if not best and match_data.get("matches"):
                best = match_data["matches"][0].get("template_id")

            template_id = best or (templates[0].id if templates else None)
            title = match_data.get("title") or templates[0].title
            difficulty = match_data.get("difficulty", "medium")

            interview_id = None
            if template_id:
                interview_data = await InterviewService.start_interview(
                    db=self.db, user_id=self.user_id, resume_id=resume_id,
                    target_position=title, difficulty=difficulty, total_questions=5
                )
                interview_id = interview_data["interview_id"]

            return {
                "success": True,
                "output": f"已匹配岗位「{title}」并创建面试",
                "interview_id": interview_id,
                "match": match_data
            }
        except Exception as e:
            logger.error(f"Agent 执行失败: {e}")
            return {"success": False, "output": str(e), "interview_id": None}

    @staticmethod
    def _parse_match_result(content: str) -> dict:
        """从 match_job_templates 返回的文本中提取 JSON"""
        try:
            # 尝试直接解析 JSON
            return json.loads(content)
        except json.JSONDecodeError:
            pass
        # 尝试从 markdown 代码块中提取
        import re
        m = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                pass
        # 尝试找到 JSON 对象
        m = re.search(r'\{[\s\S]*"best_match"[\s\S]*\}', content)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
        return {}
