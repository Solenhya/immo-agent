from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import asyncio

load_dotenv()

llm = ChatMistralAI(model="mistral-large-latest")

async def main():
    # Connexion au serveur MCP data.gouv (sans context manager, requis depuis v0.1.0)
    client = MultiServerMCPClient(
        {
            "datagouv": {
                "transport": "streamable_http",
                "url": "https://mcp.data.gouv.fr/mcp",
            }
        }
    )
    tools = await client.get_tools()
    print("Tools disponibles :")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")

    # Création de l'agent ReAct avec LangGraph
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt="You are a data assistant using French open data."
    )

    # Invocation de l'agent
    result = await agent.ainvoke({
        "messages": [("human", "Trouve le dataset sur les prix de l'immobilier en France")]
    })

    print("\nRésultat de l'agent :")

    # Récupérer le dernier message (réponse finale de l'agent)
    last_message = result["messages"][-1]
    content = last_message.content

    print(content)

    with open("result.md", "w", encoding="utf-8") as f:
        f.write(content)

    print("\nFini — résultat écrit dans result.md")

if __name__ == "__main__":
    asyncio.run(main())