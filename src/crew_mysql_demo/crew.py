# src/crew_mysql_demo/crew.py
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import agent, crew, task, CrewBase
from crewai_tools.tools.mysql_search_tool.mysql_search_tool import MySQLSearchTool
from crewai_tools.tools.nl2sql.nl2sql_tool import NL2SQLTool
from .sql_tools import RawSQLTool

@CrewBase
class MySqlReportingCrew:
    """Crew that converts NL→SQL→JSON→Report."""

    @agent
    def query_builder(self) -> Agent:
        return Agent(
            config=self.agents_config['build_sql'],
            tools=[NL2SQLTool(db_uri=os.environ['MYSQL_CREDENTIALS'])],
        )

    @agent
    def db_query(self) -> Agent:
        return Agent(
            config=self.agents_config['execute_sql'],
            tools=[RawSQLTool(db_uri=os.environ['MYSQL_CREDENTIALS'])],
        )

    @agent
    def report_generator(self) -> Agent:
        return Agent(config=self.agents_config['generate_report'], tools=[])

    @task
    def build_sql(self) -> Task:
        return Task(config=self.tasks_config['build_sql'], agent=self.query_builder())

    @task
    def execute_sql(self) -> Task:
        return Task(config=self.tasks_config['execute_sql'], agent=self.db_query())

    @task
    def generate_report(self) -> Task:
        return Task(config=self.tasks_config['generate_report'], agent=self.report_generator())

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=[self.build_sql(), self.execute_sql(), self.generate_report()],
            process=Process.sequential,
            verbose=True,
        )
