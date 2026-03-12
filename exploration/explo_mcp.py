from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langsmith import traceable
from langchain_core.messages import ToolMessage
import json
import asyncio

load_dotenv()

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
    }
)

tools = asyncio.run(client.get_tools())
print("Tools disponibles :")
print(tools)
llm = MistralMCPCompatible(model="mistral-large-latest")

#prompt = ChatPromptTemplate.from_messages([
#    ("system", "You are a data assistant using French open data."),
#    ("human", "{input}")
#])



agent = create_agent(model=llm,tools= tools, system_prompt="You are a data assistant using French open data")
#agent_executor = AgentExecutor(agent=agent, tools=tools)

@traceable
async def async_run_agent(user_message):
    messages = {"messages":[{"role":"user", "content": user_message}]}
    result = await agent.ainvoke(messages)
    return result
print("Résultat de l'agent :")
result = asyncio.run(async_run_agent("Trouve le dataset sur les prix de l'immobilier en France"))
message = result
content = message["messages"][-1].content
print(message)
with open("result.json", "w", encoding="utf-8") as f:
    f.write(content)  # Écrire le contenu directement dans le fichier
print("Fini")