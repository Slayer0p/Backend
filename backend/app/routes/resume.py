import os
import uuid
import json
import re

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.resume_parser import parse_resume
from app.services.prompts import resume_analysis_prompt
from app.services.llm import call_llm
from app.state.resume_store import (
    save_resume_text,
    save_resume_analysis,
    get_resume_text,
    get_resume_analysis,
)

router = APIRouter(prefix="/resume", tags=["Resume"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# Upload Resume
# =========================
@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(await file.read())

    resume_text = parse_resume(filepath)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not read resume")

    save_resume_text(resume_text)

    return {
        "success": True,
        "message": "Resume uploaded & processed",
    }


# =========================
# Analyze Resume (LLM)
# =========================
@router.post("/analyze")
def analyze_resume():
    resume_text = get_resume_text()
    if not resume_text:
        raise HTTPException(status_code=400, detail="No resume uploaded")

    prompt = resume_analysis_prompt(resume_text)
    raw_output = call_llm(prompt)

    print("===== LLM RAW OUTPUT =====")
    print(raw_output)
    print("TYPE:", type(raw_output))
    print("==========================")

    # ✅ CASE 1: LLM already returned parsed JSON (dict)
    if isinstance(raw_output, dict):
        save_resume_analysis(raw_output)
        print("✅ SAVED ANALYSIS (DICT)")
        return raw_output

    # ✅ CASE 2: LLM returned string → extract JSON
    if isinstance(raw_output, str):
        match = re.search(r"\{[\s\S]*\}", raw_output)
        if not match:
            print("❌ No JSON found in LLM output")
            return {
                "strong": [],
                "average": [],
                "missing": [],
            }

        try:
            parsed = json.loads(match.group())
            save_resume_analysis(parsed)
            print("✅ SAVED ANALYSIS (STRING)")
            return parsed

        except Exception as e:
            print("❌ JSON parsing failed:", e)
            return {
                "strong": [],
                "average": [],
                "missing": [],
            }

    # ❌ Fallback (should never happen)
    print("❌ Unsupported LLM output type")
    return {
        "strong": [],
        "average": [],
        "missing": [],
    }


# =========================
# Get Stored Analysis
# =========================
@router.get("/analysis")
def get_analysis():
    analysis = get_resume_analysis()
    if not analysis:
        return {
            "strong": [],
            "average": [],
            "missing": [],
        }
    return analysis
