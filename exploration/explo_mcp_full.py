from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langsmith import traceable
from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import InMemorySaver  
from langchain_mcp_adapters.interceptors import MCPToolCallRequest
import json
import asyncio

load_dotenv()

async def retry_interceptor(
    request: MCPToolCallRequest,
    handler,
    max_retries: int = 3,
    delay: float = 1.0,
):
    """Retry failed tool calls with exponential backoff."""
    last_error = None
    for attempt in range(max_retries):
        try:
            return await handler(request)
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                wait_time = delay * (2 ** attempt)  # Exponential backoff
                print(f"Tool {request.name} failed (attempt {attempt + 1}), retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
    raise last_error


class MistralMCPCompatible(ChatMistralAI):
    """Normalizes MCP tool result messages to plain strings before sending to Mistral."""
    
    def _normalize_messages(self, messages):
        normalized = []
        for msg in messages:
            if isinstance(msg, ToolMessage) and isinstance(msg.content, list):
                plain_text = "\n".join(
                    block["text"]
                    for block in msg.content
                    if isinstance(block, dict) and "text" in block
                )
                msg = ToolMessage(
                    content=plain_text,
                    tool_call_id=msg.tool_call_id,
                    name=msg.name,
                )
            normalized.append(msg)
        return normalized

    def invoke(self, messages, config=None, **kwargs):
        return super().invoke(self._normalize_messages(messages), config=config, **kwargs)

    async def ainvoke(self, messages, config=None, **kwargs):
        return await super().ainvoke(self._normalize_messages(messages), config=config, **kwargs)

# connexion au serveur MCP data.gouv
client = MultiServerMCPClient(
    {
        "datagouv": {
            "transport": "http",
            "url": "https://mcp.data.gouv.fr/mcp",
        }
    },
    tool_interceptors=[retry_interceptor],
)

tools = asyncio.run(client.get_tools())
llm = MistralMCPCompatible(model="mistral-large-latest")

#prompt = ChatPromptTemplate.from_messages([
#    ("system", "You are a data assistant using French open data."),
#    ("human", "{input}")
#])

system_prompt = """Tu es un assistant d'exploration des données accessible via le MCP de data.gouv.fr.
Ne réponds que par des données ou des analyses basées sur les données disponibles via les outils du MCP. Tu peux demander a l'utilisateur de préciser sa requète.
Ne donne pas d'exemple fictif."""

agent = create_agent(model=llm,tools= tools, system_prompt=system_prompt,checkpointer=InMemorySaver(),)
#agent_executor = AgentExecutor(agent=agent, tools=tools)
config = {"configurable": {"thread_id": "1"}}
#@traceable
async def async_run_agent(user_message):
    messages = {"messages":[{"role":"user", "content": user_message}]}
    result = await agent.ainvoke(messages, config=config)
    return result


async def cli_agent():
    while True:
        user_input = input("Entrez votre message (ou 'exit' pour quitter) : ")
        if user_input.lower() == "exit":
            print("Au revoir !")
            break
        if user_input.strip() == "":
            print("Veuillez entrer un message non vide.")
            continue
        result = await async_run_agent(user_input)
        print("Résultat de l'agent :")
        content = result["messages"][-1].content
        print(content)


if __name__ == "__main__":
    asyncio.run(cli_agent())