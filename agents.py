import os
from crewai import Agent
from crewai_tools import FileWriterTool

# Initialize tools
file_writer_tool = FileWriterTool()

def get_researcher():
    return Agent(
        role='Senior Research Analyst',
        goal='Identify the best technologies and design trends for {topic}',
        backstory='Expert in tech trends and market analysis with 10 years of experience.',
        llm='groq/llama-3.3-70b-versatile',
        verbose=True
    )

def get_developer():
    return Agent(
        role='Full Stack Web Developer',
        goal='Write clean, efficient HTML, CSS, and JS code for {topic}',
        backstory='Specialist in building responsive and interactive 3D web applications.',
        llm='groq/llama-3.3-70b-versatile',
        tools=[file_writer_tool],
        verbose=True
    )

def get_manager():
    return Agent(
        role='Project Manager',
        goal='Coordinate the workflow and ensure the project meets all requirements.',
        backstory='High-level strategist focused on efficiency and output quality.',
        llm='groq/llama-3.3-70b-versatile',
        verbose=True
    )

def get_qa_engineer():
    return Agent(
        role='QA Engineer',
        goal='Test the final code for bugs and ensure high-quality UI/UX.',
        backstory='Perfectionist focused on debugging and performance optimization.',
        llm='groq/llama-3.3-70b-versatile',
        verbose=True
    )