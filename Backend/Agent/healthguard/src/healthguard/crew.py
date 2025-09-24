import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from langchain_groq import ChatGroq
from .tools.custom_tool import (
    BrowserTool, 
    WebSearchTool
)


@CrewBase
class Healthguard():
    """Healthguard crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self) -> None:
        self.groq_llm = ChatGroq(
            model="groq/llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )

    @agent
    def nurse_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['nurse_agent'], 
            llm=self.groq_llm,
            tools=[BrowserTool(), WebSearchTool()],
            verbose=True
        )

    @agent
    def med_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['med_agent'],
            llm=self.groq_llm,
         
            verbose=True
        )

    @agent
    def labs_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['labs_agent'],
            llm=self.groq_llm,
            
            verbose=True
        )

    @agent
    def guardian_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['guardian_agent'],
            llm=self.groq_llm,
            verbose=True
        )

    @agent
    def voice_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['voice_agent'],
            llm=self.groq_llm,
     
            verbose=True
        )

    @task
    def nurse_task(self) -> Task:
        return Task(
            config=self.tasks_config['nurse_task'],
            agent=self.nurse_agent()
        )

    @task
    def med_task(self) -> Task:
        return Task(
            config=self.tasks_config['med_task'],
            agent=self.med_agent()
        )

    @task
    def labs_task(self) -> Task:
        return Task(
            config=self.tasks_config['labs_task'],
            agent=self.labs_agent()
        )

    @task
    def guardian_task(self) -> Task:
        return Task(
            config=self.tasks_config['guardian_task'],
            agent=self.guardian_agent()
        )

    @task
    def voice_task(self) -> Task:
        return Task(
            config=self.tasks_config['voice_task'],
            agent=self.voice_agent()
        )



    @crew
    def crew(self) -> Crew:
        """Creates the Healthguard crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

    def run_single_agent(self, agent_name: str, inputs: dict):
        """Run a single agent by name"""
        agent_map = {
            'nurse': (self.nurse_agent(), self.nurse_task()),
            'med': (self.med_agent(), self.med_task()),
            'labs': (self.labs_agent(), self.labs_task()),
            'guardian': (self.guardian_agent(), self.guardian_task()),
            'voice': (self.voice_agent(), self.voice_task())
        }

        if agent_name not in agent_map:
            raise ValueError(f"Unknown agent: {agent_name}. Available agents: {list(agent_map.keys())}")

        agent, task = agent_map[agent_name]

        # Create a crew with just this agent and task
        single_crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        return single_crew.kickoff(inputs=inputs)
