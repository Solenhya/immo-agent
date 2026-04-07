#!/usr/bin/env python3
"""
Entry point: Start the CLI interactive chat
"""
import asyncio
import sys

if __name__ == "__main__":
    print("🏠 AGENT IMMOBILIER (VERSION ACTION)")
    print("💬 Tapez 'exit' ou 'q' pour quitter\n")
    
    try:
        # Import here to avoid issues on startup
        from immo_agent.main import main
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✋ Arrêt de l'agent")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
