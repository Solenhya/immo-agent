import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    print("Connexion à https://mcp.data.gouv.fr/mcp (Streamable HTTP)...")
    async with streamable_http_client("https://mcp.data.gouv.fr/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            print("Initialisation...")
            await session.initialize()
            
            # --- 1. Lister les outils ---
            print("\n=== TOUS LES OUTILS DISPONIBLES ===")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"- {tool.name}")
            
            # --- 2. Voir le résultat d'une recherche précise ---
            query = "Recensement des équipements sportifs"
            print(f"\n=== RECHERCHE : '{query}' ===")
            result = await session.call_tool("search_datasets", arguments={"query": query})
            
            if result.content:
                # J'enlève le [:500] pour tout afficher
                print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
