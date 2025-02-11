import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
import json

# Load JSON file
with open("data/context.json", "r") as file:
    json_data = json.load(file)


load_dotenv(dotenv_path='./config/.env')

# Initialize Large Language Model (LLM) of your choice (see all models on our Models page)
llm = LLM(model="groq/llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

# Create your CrewAI agents with role, main goal/objective, and backstory/personality
summarizer = Agent(
    role='json Summarizer', # Agent's job title/function
    goal='Create concise summaries of json info', # Agent's main objective
    backstory='Technical writer who excels at extracting and formatting all relevant useful data', # Agent's background/expertise
    llm=llm, # LLM that powers your agent
    verbose=True # Show agent's thought process as it completes its task
)


summary_task = Task(
    description=f'Summarize the following JSON data: {json.dumps(json_data)}',
    expected_output="A clear, concise summary in points",
    agent=summarizer,
    output_file="data/context.txt"
)


# Create crew to manage agents and task workflow
crew = Crew(
    agents=[summarizer], # Agents to include in your crew
    tasks=[summary_task], # Tasks in execution order
    verbose=True
)

result = crew.kickoff()
