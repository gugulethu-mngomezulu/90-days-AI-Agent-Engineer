from pydantic import BaseModel, Field


class ResumeAnalysis(BaseModel):
    candidate_name: str
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    recommendations: list[str]
    summary: str


class SkillMatchResult(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    match_percentage: float = Field(ge=0, le=100)