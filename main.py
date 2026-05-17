from fastapi import FastAPI
from groq import Groq
import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task

load_dotenv()

app = FastAPI()

# Groq API Key Setup for CrewAI
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama-3.1-8b-instant"
os.environ["OPENAI_API_KEY"] = os.environ.get("GROQ_API_KEY")

@app.get("/")
def home():
    return {
        "status": "Online",
        "message": "Fadii AI Swarm Agency is Live",
        "owner": "Fawad Awan"
    }

@app.get("/agency")
def run_agency(topic: str):
    try:
        # 1. Define the SEO Expert Agent
        seo_expert = Agent(
            role="Senior SEO & Keywords Specialist",
            goal=f"Analyze and create a high-ranking SEO strategy for the topic: {topic}",
            backstory="You are an expert in search engine optimization. You find high-traffic, low-competition keywords and structure perfect content outlines.",
            verbose=True,
            allow_delegation=False
        )

        # 2. Define the Content Writer Agent
        content_writer = Agent(
            role="Professional Content Writer",
            goal=f"Write a comprehensive, engaging, and SEO-optimized blog post about {topic}",
            backstory="You are a brilliant tech and business blogger. You take SEO outlines and turn them into highly engaging, human-like articles that rank on Google.",
            verbose=True,
            allow_delegation=False
        )

        # 3. Define Tasks for the Agents
        task1 = Task(
            description=f"Identify 5 high-potential keywords and create a complete SEO content outline for the topic: {topic}.",
            expected_output="A structured markdown outline with keywords, headings (H1, H2, H3), and search intent analysis.",
            agent=seo_expert
        )

        task2 = Task(
            description=f"Using the outline from Task 1, write a full blog post. Ensure the keywords are naturally integrated and the tone is professional.",
            expected_output="A complete, ready-to-publish blog post in markdown format.",
            agent=content_writer
        )

        # 4. Form the Crew (The Agent Swarm)
        crew = Crew(
            agents=[seo_expert, content_writer],
            tasks=[task1, task2],
            process=Process.sequential
        )

        # 5. Kickoff the process
        result = crew.kickoff()
        
        return {"agency_response": str(result)}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
