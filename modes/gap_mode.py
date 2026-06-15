# modes/gap_mode.py
from crewai import Task, Crew
from agents import get_resume_agent, get_job_agent, get_ranking_agent
import json, re

def run_gap_mode(resume_text: str, jd_text: str):
    resume_agent = get_resume_agent()
    job_agent = get_job_agent()
    ranking_agent = get_ranking_agent()

    tasks = [
        Task(
            description=f"Extract candidate details from this resume:\n\n{resume_text}",
            expected_output="JSON with candidate_name, skills, experience_years, education.",
            agent=resume_agent
        ),
        Task(
            description=f"Extract all requirements from this job description:\n\n{jd_text}",
            expected_output="JSON with job_title, required_skills, experience_years, qualifications.",
            agent=job_agent
        ),
        Task(
            description="Compare resume against job description in detail. Find exact skill gaps.",
            expected_output="JSON with match_score, matched_skills (list), missing_skills (list), recommendations (list). No markdown, pure JSON only.",
            agent=ranking_agent
        )
    ]

    crew = Crew(agents=[resume_agent, job_agent, ranking_agent], tasks=tasks)
    output = crew.kickoff()

    try:
        raw = str(output).strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        data = json.loads(raw)
    except:
        data = {"raw_output": str(output)}

    return data