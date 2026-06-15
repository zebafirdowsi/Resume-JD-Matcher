from crewai import Agent
import os

def get_job_agent() -> Agent:
    return Agent(
        role="Job Description Parser Agent",
        goal="Extract required skills, qualifications, and experience from the provided job description text.",
        backstory="Specialist in understanding what companies look for in candidates.",
        verbose=True,
        llm=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    )