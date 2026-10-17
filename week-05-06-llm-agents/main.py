from llm_client import analyze_resume
from agent import run_agent


RESUME = """
Candidate: Alex Mokoena

Junior Python Developer

Skills:
- Python
- FastAPI
- PostgreSQL
- Git
- Docker

Experience:
Built REST APIs using FastAPI.
Worked with PostgreSQL databases.
Used Git for version control.
Created Docker containers for development.
"""


JOB_DESCRIPTION = """
Junior AI Backend Developer

Required Skills:
- Python
- FastAPI
- PostgreSQL
- Docker
- REST APIs
- LangChain
- Redis

Responsibilities:
Build and maintain backend APIs.
Integrate AI services with Python applications.
Work with databases and containerized applications.
"""


RESUME_SKILLS = [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "Git",
    "Docker",
    "REST APIs",
]

REQUIRED_SKILLS = [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "Docker",
    "REST APIs",
    "LangChain",
    "Redis",
]


def main():

    print("=" * 55)
    print("AI RESUME ANALYZER AGENT")
    print("Week 5 + 6 | 90 Days of AI Agent Engineering")
    print("=" * 55)

    # WEEK 5
    print("\n========== WEEK 5 ==========")

    analysis = analyze_resume(
        resume=RESUME,
        job_description=JOB_DESCRIPTION,
    )

    print("\nSTRUCTURED RESUME ANALYSIS")
    print(analysis.model_dump_json(indent=2))

    # WEEK 6
    print("\n========== WEEK 6 ==========")

    agent_result = run_agent(
        resume_skills=RESUME_SKILLS,
        required_skills=REQUIRED_SKILLS,
    )

    print("\nFINAL AGENT RESPONSE")
    print(agent_result)

    print("\n" + "=" * 55)
    print("Week 5 + 6 demonstration complete!")
    print("=" * 55)


if __name__ == "__main__":
    main()