#!/usr/bin/env python3
"""
Entry point: Start the FastAPI web server
"""
import uvicorn
import sys

if __name__ == "__main__":
    print("🚀 Démarrage du serveur API...")
    print("📱 Accédez à: http://127.0.0.1:8000")
    print("🛑 Arrêtez avec Ctrl+C\n")
    
    try:
        uvicorn.run(
            "immo_agent.api:app",
            host="127.0.0.1",
            port=8000,
            reload=True
        )
    except KeyboardInterrupt:
        print("\n✋ Arrêt du serveur")
        sys.exit(0)
