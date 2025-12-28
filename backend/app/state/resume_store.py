# Simple in-memory store (safe for single-node apps)

_resume_text: str | None = None
_resume_analysis: dict | None = None


def save_resume_text(text: str):
    global _resume_text
    _resume_text = text


def get_resume_text() -> str | None:
    return _resume_text


def save_resume_analysis(data: dict):
    global _resume_analysis
    _resume_analysis = data


def get_resume_analysis() -> dict | None:
    return _resume_analysis
