from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from tools.custom_tool import CustomSerperDevTool
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
lm_studio = LLM(
		model="github/gpt-4.1",
		temperature= 1,
     	top_p= 1,
		api_key=GITHUB_API_KEY
	)

@CrewBase
class Day04Crew:
	"""Day04 crew"""

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[CustomSerperDevTool(), ScrapeWebsiteTool()],
			verbose=True,
			llm=lm_studio
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
			llm=lm_studio
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Day03 crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
		)