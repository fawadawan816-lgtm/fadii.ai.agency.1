import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from crewai import Crew, Task, Process
from agents import get_researcher, get_developer, get_manager, get_qa_engineer

# Load environment variables for API keys
load_dotenv()

app = FastAPI(title="Fadii AI Agentic Agency")

@app.get("/")
def health_check():
    """
    Endpoint to verify if the server is live.
    """
    return {
        "status": "online",
        "agency_name": "Fadii AI Agency",
        "active_agents": ["Researcher", "Developer", "Manager", "QA Engineer"]
    }

@app.get("/run")
async def run_agency(topic: str = "Modern 3D Portfolio Website"):
    """
    Endpoint to trigger the Agentic Workflow.
    Example: /run?topic=E-commerce Site
    """
    try:
        # 1. Initialize Agents from agents.py
        researcher = get_researcher()
        developer = get_developer()
        manager = get_manager()
        qa = get_qa_engineer()

        # 2. Define Sequential Tasks
        research_task = Task(
            description=f"Analyze the latest market trends and technical requirements for: {topic}.",
            agent=researcher,
            expected_output="A detailed technical roadmap and feature list."
        )

        development_task = Task(
            description=f"Based on the research, write the complete HTML, CSS, and JS code for {topic}. Use professional styling.",
            agent=developer,
            expected_output="Fully functional source code files."
        )

        qa_task = Task(
            description="Perform a final code review, check for responsiveness, and fix any logical bugs.",
            agent=qa,
            expected_output="A final, production-ready version of the code and a quality report."
        )

        # 3. Assemble the Crew
        fadii_crew = Crew(
            agents=[researcher, manager, developer, qa],
            tasks=[research_task, development_task, qa_task],
            process=Process.sequential,
            verbose=True
        )

        # 4. Execute the Process
        result = fadii_crew.kickoff(inputs={'topic': topic})

        return {
            "status": "success",
            "topic": topic,
            "final_output": str(result)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable for cloud deployment
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)