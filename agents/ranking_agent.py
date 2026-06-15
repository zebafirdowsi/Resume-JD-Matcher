# agents/ranking_agent.py
from crewai import Agent
import os

def get_ranking_agent() -> Agent:
    return Agent(
        role="Ranking Agent",
        goal="Compare resume and job description, give match score 0-100 with reasoning.",
        backstory="HR evaluation expert who calculates fit between candidates and roles.",
        verbose=True,
        llm=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    )