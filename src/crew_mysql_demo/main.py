import pathlib
import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class MyFirstCrew:
    @agent
    def hello(self) -> Agent:
        return Agent(
            config=self.agents_config["hello"],
            tools=[],
        )

    @task
    def say_hello(self) -> Task:
        return Task(
            config=self.tasks_config["say_hello"],
            agent=self.hello(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

def run():
    base_dir   = pathlib.Path(__file__).parent
    config_dir = base_dir / "config"

    # Load your configs with explicit UTF-8
    agents_cfg = yaml.safe_load((config_dir / "agents.yaml").read_text(encoding="utf-8"))
    tasks_cfg  = yaml.safe_load((config_dir / "tasks.yaml").read_text(encoding="utf-8"))

    # Instantiate & inject configs
    # CORRECT: operate on the CrewBase instance
    crew_base = MyFirstCrew()
    crew_base.agents_config = agents_cfg
    crew_base.tasks_config  = tasks_cfg
    # Now build the Crew and kickoff
    crew_base.crew().kickoff(inputs={})
    # Kick it off
    #crew.kickoff(inputs={})

if __name__ == "__main__":
    run()
