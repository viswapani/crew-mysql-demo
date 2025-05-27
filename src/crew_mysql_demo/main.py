# src/crew_mysql_demo/main.py
import sys
import pathlib
import yaml
import os
from crew_mysql_demo.crew import MySqlReportingCrew

def run():
    base_dir = pathlib.Path(__file__).parent
    config_dir = base_dir / "config"
    agents_cfg = yaml.safe_load((config_dir / "agents.yaml").read_text(encoding="utf-8"))
    tasks_cfg = yaml.safe_load((config_dir / "tasks.yaml").read_text(encoding="utf-8"))

    # ✅ Fully initialize CrewBase class
    crew_base = MySqlReportingCrew()
    crew_base.agents_config = agents_cfg
    crew_base.tasks_config = tasks_cfg
    crew_base.map_all_task_variables()

    question = sys.argv[1] if len(sys.argv) > 1 else "Show me sales data"
    crew_base.crew().kickoff(inputs={"question": question})

if __name__ == "__main__":
    run()
