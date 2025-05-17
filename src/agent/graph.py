"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations


from langgraph.graph import StateGraph


from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
# from langgraph.checkpoint.memory import MemorySaver
from agent.states import AgentState
from agent.tools import tools 
from agent.llm import  llm_with_tools
from langgraph.types import Command
async def chat(state: AgentState) -> AgentState:
    response = await llm_with_tools.ainvoke(state["messages"])

    return Command(update={"messages": [response]})  # đảm bảo là list of BaseMessage
# def chat(state: AgentState) -> AgentState:
#     response = llm_with_tools.invoke(state["messages"])

#     return Command(update={"messages": [response]})  # đảm bảo là list of BaseMessage


tool_node = ToolNode(tools=tools)



notes_workflow = StateGraph(AgentState)
notes_workflow.add_node("chat", chat)
notes_workflow.add_node("tools", tool_node)
notes_workflow.add_edge(START, "chat")
notes_workflow.add_conditional_edges("chat", tools_condition)
notes_workflow.add_edge("tools", "chat")
notes_workflow.set_entry_point("chat")
# memory = MemorySaver()
# Graph = notes_workflow.compile(checkpointer=memory)
graph = notes_workflow.compile()
