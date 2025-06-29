from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from .tools import tools
llm = init_chat_model("google_genai:gemini-2.0-flash")
llm_with_tools = llm.bind_tools(tools)
