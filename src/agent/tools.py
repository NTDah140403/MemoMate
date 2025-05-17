from typing import List, Annotated
from langgraph.prebuilt import InjectedState

from langchain_core.tools import tool, InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from datetime import datetime
from .states import AgentState


@tool
def save_note(tool_call_id: Annotated[str, InjectedToolCallId], content: str, state: Annotated[AgentState, InjectedState]) -> Command:
    """Save a new note with the given content"""
    new_note = {
        "id": datetime.now().timestamp(),
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    return Command(update={
        "notes": state["notes"] + [new_note],
        "messages": [
            ToolMessage(
                "Successfully looked up user information",
                tool_call_id=tool_call_id
            )
        ]
    })

# Tool: Delete a note by ID
@tool
def delete_note(
    tool_call_id: Annotated[str, InjectedToolCallId],
    note_id: float,
    state: Annotated[AgentState, InjectedState]
) -> Command:
    """Delete a note from the list by its ID."""
    updated_notes = [note for note in state["notes"] if note["id"] != note_id]
    return Command(update={
        "notes": updated_notes,
        "messages": [
            ToolMessage(
                "Successfully deleted the note.",
                tool_call_id=tool_call_id
            )
        ]
    })

# Tool: Edit a note by ID
@tool
def edit_note(
    tool_call_id: Annotated[str, InjectedToolCallId],
    note_id: float,
    new_content: str,
    state: Annotated[AgentState, InjectedState]
) -> Command:
    """Edit a note from the list by its ID."""
    updated_notes = []
    for note in state["notes"]:
        if note["id"] == note_id:
            note = note.copy()
            note["content"] = new_content
            note["timestamp"] = datetime.now().isoformat()
        updated_notes.append(note)
    return Command(update={
        "notes": updated_notes,
        "messages": [
            ToolMessage(
                "Successfully edited the note.",
                tool_call_id=tool_call_id
            )
        ]
    })

# Tool: List notes
@tool
def list_notes(state: Annotated[AgentState, InjectedState]) -> str:
    """List all notes."""
    if not state["notes"]:
        return "No notes found."
    return state["notes"]
# Tools list
tools = [save_note, delete_note, edit_note, list_notes]
