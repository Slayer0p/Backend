import json
import re
from openai import OpenAI
from app.core.config import get_settings

settings = get_settings()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=settings.OPENAI_API_KEY,
)

def extract_json(text: str) -> dict:
    """
    Extract first valid JSON object from text
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found")

    return json.loads(match.group())


def call_llm(prompt: str) -> dict:
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3.2:novita",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an API endpoint. "
                    "You MUST return ONLY a valid JSON object. "
                    "Do NOT include markdown, explanations, or extra text."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    # 🔥 DEBUG — THIS IS IMPORTANT
    print("\n===== LLM RAW OUTPUT =====\n")
    print(content)
    print("\n==========================\n")

    try:
        return extract_json(content)
    except Exception as e:
        print("❌ JSON PARSE FAILED:", e)
        return {}
