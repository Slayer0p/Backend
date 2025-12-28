from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List

from app.services.llm import call_llm
from app.state.resume_store import get_resume_text, get_resume_analysis

router = APIRouter(prefix="/interview", tags=["Interview"])


# ---------- Schemas ----------
class Question(BaseModel):
    id: int
    question: str
    answer: str
    category: str


class InterviewResponse(BaseModel):
    beginner: List[Question]
    intermediate: List[Question]
    advanced: List[Question]


# ---------- Route ----------
@router.get("/", response_model=InterviewResponse)
def interview_questions(role: str = Query(...)):
    resume_text = get_resume_text()
    analysis = get_resume_analysis()

    if not resume_text or not analysis:
        raise HTTPException(
            status_code=400,
            detail="Resume not analyzed yet"
        )

    strong = [s["name"] for s in analysis.get("strong", [])]
    average = [s["name"] for s in analysis.get("average", [])]
    missing = [s["name"] for s in analysis.get("missing", [])]

    prompt = f"""
You are an expert technical interviewer.

Candidate Resume:
\"\"\"
{resume_text}
\"\"\"

Target Role: {role}

Candidate Skills:
- Strong: {strong}
- Average: {average}
- Missing: {missing}

TASK:
- Focus more on weak & missing skills
- Ask fewer questions from strong skills
- Avoid irrelevant questions
- Provide correct answers

Return ONLY valid JSON in this EXACT format:

{{
  "beginner": [
    {{
      "id": 1,
      "question": "string",
      "answer": "string",
      "category": "string"
    }}
  ],
  "intermediate": [],
  "advanced": []
}}
"""

    result = call_llm(prompt)

    # ✅ IMPORTANT: LLM ALREADY RETURNS DICT
    if not result or "beginner" not in result:
        raise HTTPException(
            status_code=500,
            detail="Invalid interview questions generated"
        )

    return result
