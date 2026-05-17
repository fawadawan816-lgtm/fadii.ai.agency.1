from fastapi import FastAPI
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

@app.get("/")
def home():
    return {
        "status": "Online",
        "message": "Fadii AI Custom Swarm Agency is Live",
        "owner": "Fawad Awan"
    }

@app.get("/agency")
def run_agency(topic: str):
    try:
        # --- AGENT 1: SEO EXPERT ---
        seo_prompt = f"""
        You are a Senior SEO & Keywords Specialist.
        Analyze and create a high-ranking SEO strategy for the topic: '{topic}'.
        Identify 5 high-potential keywords and create a complete structured content outline (H1, H2, H3).
        """
        
        seo_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": seo_prompt}],
            model="llama-3.1-8b-instant",
        )
        seo_output = seo_completion.choices[0].message.content

        # --- AGENT 2: CONTENT WRITER ---
        writer_prompt = f"""
        You are a Professional Content Writer.
        Using the following SEO Outline and Keywords, write a comprehensive, engaging, and highly optimized blog post.
        Ensure the keywords are naturally integrated and the tone is professional.
        
        SEO OUTLINE PROVIDED BY SEO EXPERT:
        {seo_output}
        """
        
        writer_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": writer_prompt}],
            model="llama-3.1-8b-instant",
        )
        final_blog_post = writer_completion.choices[0].message.content

        return {
            "topic": topic,
            "seo_agent_strategy": seo_output,
            "writer_agent_article": final_blog_post
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
