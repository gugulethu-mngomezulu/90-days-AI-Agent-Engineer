import os

from dotenv import load_dotenv
from schemas import ResumeAnalysis

load_dotenv()

MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

client = None

if not MOCK_MODE:
    from openai import OpenAI
    client = OpenAI()


def analyze_resume(resume: str, job_description: str) -> ResumeAnalysis:

    print("\n[WEEK 5] Starting resume analysis...")

    if MOCK_MODE:
        print("[MOCK MODE] Using simulated LLM response.")

        mock_response = {
            "candidate_name": "Gugulethu Mngomezulu",
            "matched_skills": [
                "Python",
                "FastAPI",
                "PostgreSQL",
                "Docker",
                "REST APIs",
            ],
            "missing_skills": [
                "LangChain",
                "Redis",
            ],
            "strengths": [
                "Python backend development",
                "REST API development",
                "Database experience",
            ],
            "recommendations": [
                "Learn LangChain fundamentals",
                "Explore Redis caching",
                "Build an AI-powered backend project",
            ],
            "summary": (
                "The candidate demonstrates relevant backend "
                "development skills, with opportunities to "
                "strengthen AI framework and caching knowledge."
            ),
        }

        result = ResumeAnalysis.model_validate(mock_response)

        print("[WEEK 5] Mock structured output validated!")
        return result

    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful resume analysis assistant. "
                    "Compare the resume against the job description. "
                    "Only identify skills supported by the supplied text. "
                    "Provide clear recommendations."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"RESUME:\n{resume}\n\n"
                    f"JOB DESCRIPTION:\n{job_description}"
                ),
            },
        ],
        response_format=ResumeAnalysis,
        temperature=0,
    )

    message = response.choices[0].message

    if message.refusal:
        raise ValueError(f"Model refused: {message.refusal}")

    if message.parsed is None:
        raise ValueError("No valid structured response returned.")

    return message.parsed