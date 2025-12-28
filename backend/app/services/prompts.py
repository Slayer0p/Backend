def interview_prompt(role: str) -> str:
    return f"""
You are an interview question generator.

Generate interview questions for the role: {role}.

Return ONLY valid JSON.
NO markdown.
NO explanation.
NO extra keys.

JSON format (EXACT):

{{
  "beginner": [
    {{
      "id": 1,
      "question": "string",
      "answer": "string",
      "category": "string"
    }}
  ],
  "intermediate": [
    {{
      "id": 2,
      "question": "string",
      "answer": "string",
      "category": "string"
    }}
  ],
  "advanced": [
    {{
      "id": 3,
      "question": "string",
      "answer": "string",
      "category": "string"
    }}
  ]
}}

Rules:
- ids must be unique integers
- include 3–6 questions per level if possible
- categories must be technical (e.g., Backend, React, System Design)
- do not repeat questions across levels
"""


def roadmap_prompt(duration: str) -> str:
    return f"""
You are an AI learning roadmap generator.

Create a {duration}-day learning roadmap.

Return ONLY valid JSON.
NO markdown.
NO explanation.
NO extra keys.

JSON format (EXACT):

{{
  "thirtyDay": [
    {{
      "week": 1,
      "title": "Week title",
      "tasks": [
        {{
          "id": 1,
          "title": "Task title",
          "duration": "2 hours",
          "completed": false
        }}
      ]
    }}
  ]
}}

Rules:
- week must be an integer starting from 1
- task ids must be unique integers
- duration must be a string (e.g., "2 hours")
- completed must be false
- include realistic backend-focused tasks
"""

def resume_analysis_prompt(resume_text: str) -> str:
    return f"""
You are an AI resume analyzer.

Analyze the resume text and classify ONLY technical skills into:
- strong
- average
- missing

Return ONLY valid JSON.
NO markdown.
NO explanation.
NO extra keys.

JSON format (EXACT):

{{
  "strong": [
    {{ "name": "Skill", "level": 80 }}
  ],
  "average": [
    {{ "name": "Skill", "level": 60 }}
  ],
  "missing": [
    {{ "name": "Skill", "recommended": true }}
  ]
}}

Rules:
- skills must be real technical skills (languages, frameworks, tools)
- do NOT include soft skills
- level must be between 40 and 95
- include 3–6 skills per section if possible
- recommended must be true for missing skills

Resume text:
\"\"\"
{resume_text[:6000]}
\"\"\"
"""
