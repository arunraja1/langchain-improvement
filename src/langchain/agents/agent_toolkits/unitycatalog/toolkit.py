"""Toolkit for interacting with an SQL database."""
from typing import List

from pydantic_v1 import Field

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import BaseTool
from langchain.tools.sql_database.tool import (
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain.tools.unitycatalog_database.tool import (
    InfoUnityCatalogTool
)
from langchain.utilities.sql_database import SQLDatabase


class UCSQLDatabaseToolkit(BaseToolkit):
    """Toolkit for interacting with Unity Catalog SQL databases."""
    db: SQLDatabase = Field(exclude=True)
    llm: BaseLanguageModel = Field(exclude=True)
    db_token : str
    db_host : str
    db_catalog : str
    db_schema : str
    db_warehouse_id : str
    allow_extra_fields = True


    @property
    def dialect(self) -> str:
        """Return string representation of SQL dialect to use."""
        return self.db.dialect

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        list_sql_database_tool = ListSQLDatabaseTool(db=self.db)
        info_sql_database_tool_description = (
            "Input to this tool is a comma-separated list of tables, output is the "
            "schema and sample rows for those tables. "
            "Be sure that the tables actually exist by calling "
            f"{list_sql_database_tool.name} first! "
            "Example Input: 'table1, table2, table3'"
        )
        info_sql_database_tool = InfoUnityCatalogTool(
            db=self.db, 
            description=info_sql_database_tool_description,
            db_token  = self.db_token ,
            db_host = self.db_host ,
            db_catalog = self.db_catalog ,
            db_schema = self.db_schema ,
            db_warehouse_id = self.db_warehouse_id
        )
        query_sql_database_tool_description = (
            "Input to this tool is a detailed and correct SQL query, output is a "
            "result from the database. If the query is not correct, an error message "
            "will be returned. If an error is returned, rewrite the query, check the "
            "query, and try again. If you encounter an issue with Unknown column "
            f"'xxxx' in 'field list', using {info_sql_database_tool.name} "
            "to query the correct table fields."
        )
        query_sql_database_tool = QuerySQLDataBaseTool(
            db=self.db, description=query_sql_database_tool_description
        )
        query_sql_checker_tool_description = (
            "Use this tool to double check if your query is correct before executing "
            "it. Always use this tool before executing a query with "
            f"{query_sql_database_tool.name}!"
        )
        query_sql_checker_tool = QuerySQLCheckerTool(
            db=self.db, llm=self.llm, description=query_sql_checker_tool_description
        )
        return [
            query_sql_database_tool,
            info_sql_database_tool,
            list_sql_database_tool,
            query_sql_checker_tool,
        ]
