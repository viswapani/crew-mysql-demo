from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import NL2SQLTool
import os
from sqlalchemy import create_engine, text
from typing import Any, List, Dict

# RawSQLTool defined in this module
class RawSQLTool:
    def __init__(self, config: Dict[str, Any]):
        # expects config={'db_uri': str}
        self.db_uri = config['db_uri']

    def run(self, prompt: str) -> List[Dict[str, Any]]:
        engine = create_engine(self.db_uri)
        with engine.connect() as conn:
            result = conn.execute(text(prompt))
        return [dict(row) for row in result]

@CrewBase
class CrewAutomationForMysqlReportingAndVisualizationsCrew:
    """Crew for MySQL reporting and visualizations"""

    @agent
    def ui_interaction(self) -> Agent:
        return Agent(
            config=self.agents_config['ui_interaction'],
            tools=[]
        )

    @agent
    def query_builder(self) -> Agent:
        return Agent(
            config=self.agents_config['query_builder'],
            tools=[ NL2SQLTool(db_uri=os.environ['MYSQL_CREDENTIALS']) ]
        )

    @agent
    def db_query(self) -> Agent:
        db_uri = os.environ['MYSQL_CREDENTIALS']
        return Agent(
            config=self.agents_config['db_query'],
            tools=[
                {
                    "class_path": "crew_automation_for_mysql_reporting_and_visualizations.crew.RawSQLTool",
                    "name": "raw_sql_tool",
                    "description": "Execute raw SQL against MySQL",
                    "config": {"db_uri": db_uri}
                }
            ]
        )

    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator'],
            tools=[]
        )

    @agent
    def validation(self) -> Agent:
        return Agent(
            config=self.agents_config['validation'],
            tools=[]
        )

    @task
    def capture_user_input(self) -> Task:
        return Task(
            config=self.tasks_config['capture_user_input'],
            agent=self.ui_interaction()
        )

    @task
    def build_sql_query(self) -> Task:
        return Task(
            config=self.tasks_config['build_sql_query'],
            agent=self.query_builder()
        )

    @task
    def execute_sql_query(self) -> Task:
        return Task(
            config=self.tasks_config['execute_sql_query'],
            agent=self.db_query()
        )

    @task
    def generate_report(self) -> Task:
        return Task(
            config=self.tasks_config['generate_report'],
            agent=self.report_generator()
        )

    @task
    def validate_report(self) -> Task:
        return Task(
            config=self.tasks_config['validate_report'],
            agent=self.validation()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
