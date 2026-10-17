from schemas import SkillMatchResult


def calculate_skill_match(
    resume_skills: list[str],
    required_skills: list[str],
) -> dict:
    """Calculate keyword overlap between resume and job skills."""

    def normalize(skills: list[str]) -> dict[str, str]:
        return {
            skill.strip().casefold(): skill.strip()
            for skill in skills
            if skill.strip()
        }

    resume = normalize(resume_skills)
    required = normalize(required_skills)

    matched = [
        skill for key, skill in required.items()
        if key in resume
    ]

    missing = [
        skill for key, skill in required.items()
        if key not in resume
    ]

    percentage = (
        round(len(matched) / len(required) * 100, 2)
        if required else 0.0
    )

    result = SkillMatchResult(
        matched_skills=matched,
        missing_skills=missing,
        match_percentage=percentage,
    )

    return result.model_dump()


TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "calculate_skill_match",
        "description": (
            "Calculate simple skill overlap between "
            "resume skills and job requirements."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "resume_skills": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "required_skills": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": [
                "resume_skills",
                "required_skills",
            ],
            "additionalProperties": False,
        },
    },
}