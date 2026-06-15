# modes/hr_mode.py
from crewai import Task, Crew
from agents import get_resume_agent, get_job_agent, get_ranking_agent
import json, re

def run_hr_mode(jd_text: str, resume_texts: list, top_n: int = 3):
    results = []

    job_agent = get_job_agent()

    for resume_text in resume_texts:
        resume_agent = get_resume_agent()
        ranking_agent = get_ranking_agent()

        tasks = [
            Task(
                description=f"Extract all requirements from this job description:\n\n{jd_text}",
                expected_output="JSON with required_skills, experience_years, qualifications.",
                agent=job_agent
            ),
            Task(
                description=f"Extract candidate details from this resume:\n\n{resume_text}",
                expected_output="JSON with candidate_name, skills, experience_years, education.",
                agent=resume_agent
            ),
            Task(
                description="Compare the resume details against job requirements. Give match score out of 100.",
                expected_output="JSON with candidate_name, match_score, strengths (list), gaps (list). No markdown, pure JSON only.",
                agent=ranking_agent
            )
        ]

        crew = Crew(agents=[job_agent, resume_agent, ranking_agent], tasks=tasks)
        output = crew.kickoff()

        try:
            raw = str(output).strip()
            raw = re.sub(r"```json|```", "", raw).strip()
            data = json.loads(raw)
        except:
            data = {"raw_output": str(output), "match_score": 0}

        results.append(data)

    sorted_results = sorted(results, key=lambda x: x.get("match_score", 0), reverse=True)
    return sorted_results[:top_n]