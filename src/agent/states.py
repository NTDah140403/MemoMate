from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

from typing import List, Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages,BaseMessage

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages] 
    notes: List[dict] 
