import asyncio
import sys
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# Création du serveur MCP
server = Server("weather-test-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Liste les outils disponibles sur ce serveur MCP"""
    return [
        types.Tool(
            name="get_weather",
            description="Récupère la météo en temps réel pour une ville donnée",
            inputSchema={
                "type": "object",
                "properties": {
                    "ville": {"type": "string"},
                },
                "required": ["ville"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Exécute l'outil demandé"""
    # On écrit dans stderr car stdout est réservé au protocole JSON-RPC du MCP
    sys.stderr.write(f"DEBUG: Appel de l'outil MCP {name} avec {arguments}\n")
    if name == "get_weather":
        ville = arguments.get("ville", "Inconnue")
        # On simule une réponse de serveur distant
        return [types.TextContent(type="text", text=f"Météo à {ville} : Ensoleillé, 22°C (Réponse via serveur MCP Local).")]
    raise ValueError(f"Outil inconnu: {name}")

async def main():
    # Le serveur communique via Standard Input/Output
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weather-test-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
