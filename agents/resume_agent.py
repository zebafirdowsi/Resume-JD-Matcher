# agents/resume_agent.py
from crewai import Agent
import os

def get_resume_agent() -> Agent:
    return Agent(
        role="Resume Parser Agent",
        goal="Extract candidate skills, experience, and education from the resume text provided in the task.",
        backstory="Expert recruiter who reads resumes thoroughly.",
        verbose=True,
        llm=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    )