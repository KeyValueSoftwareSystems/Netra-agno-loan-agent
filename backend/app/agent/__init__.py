"""Nova Loan Agent — built with Agno."""

import logging
import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb

from agent.prompt import get_system_prompt
from agent.tools import AGENT_TOOLS

_DB_PATH = os.environ.get("DATABASE_PATH", "data/nova.db")

agent = Agent(
    name="Nova Agent",
    model=OpenAIChat(id="gpt-4.1"),
    instructions=get_system_prompt(),
    tools=AGENT_TOOLS,
    db=SqliteDb(db_file=_DB_PATH),
    add_history_to_context=True,
    num_history_runs=20,
    markdown=True,
)


async def get_response(prompt: str, session_id: str) -> str:
    """Run the agent and return the text response."""
    logging.info(f"Agent invoked — session_id={session_id}, prompt length={len(prompt)}")
    response = await agent.arun(prompt, session_id=session_id)
    content = response.content if response and response.content else ""
    logging.info(f"Agent responded — session_id={session_id}, response length={len(content)}")
    return content
