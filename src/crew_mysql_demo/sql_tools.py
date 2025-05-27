# src/crew_mysql_demo/sql_tools.py
import os
from pydantic import PrivateAttr
from sqlalchemy import create_engine, text
from typing import Any, List, Dict
from crewai.tools import BaseTool  # works if crewai >= 0.121.0

class RawSQLTool(BaseTool):
    def __init__(self, db_uri: str):
        # Set name & description as instance fields (not ClassVar)
        super().__init__(
            name="raw_sql",
            description="Executes the given SQL and returns rows as dicts."
        )
        self._db_uri: str = db_uri  # private field not tracked by Pydantic

    def _run(self, sql_query: str) -> List[Dict[str, Any]]:
        engine = create_engine(self._db_uri)
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            return list(result.mappings())  #Correct and safe
            #return [dict(row) for row in result]
