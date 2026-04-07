# 📁 Structure du projet immo-agent

```
immo-agent/
│
├── immo_agent/                 📦 Package principal (code source)
│   ├── __init__.py
│   ├── runIA.py               🔧 Définition des outils IA & LLM
│   ├── api.py                 🌐 API FastAPI
│   ├── main.py                💬 CLI interactive
│   ├── agent_memory.py        🧠 Gestion de la mémoire (langgraph)
│   ├── api_auth.py            🔐 Authentification
│   ├── db_session.py          💾 Gestion sessions BD
│   ├── check_setup.py         ✅ Vérification configuration
│   ├── csv_to_sqlite.py       📊 Import données CSV
│   ├── init_and_run.py        🚀 Initialisation
│   ├── test_mcp.py            🧪 Tests MCP
│   └── weather_mcp.py         🌤️ MCP serveur météo
│
├── scripts/                    🎯 Points d'entrée
│   ├── run_api.py             → python scripts/run_api.py
│   └── run_cli.py             → python scripts/run_cli.py
│
├── frontend/                   🎨 Interface web
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── auth.js
│
├── data/                       📊 Données
│   ├── immo_ventes.db         (SQLite - DVF data)
│   ├── memory.db              (historique conversations)
│   ├── auth_system.db
│   └── ValeursFoncieres-2025-S1.csv
│
├── documentation/              📚 Documentation
│   ├── benchmark projIA.md
│   └── note-cadrage projIA.md
│
├── exploration/                🔍 Scripts d'exploration
│   ├── expl_mcp.py
│   ├── expl_mcp2.py
│   ├── expl_mcp_full.py
│   ├── explograph.py
│   ├── explograph2.py
│   └── explotools.py
│
├── tests/                      🧪 Tests unitaires
│   └── __init__.py
│
├── config/                     ⚙️ Configuration
│   └── settings.py             (paramètres globaux)
│
├── .env.example                (À copier en .env)
├── .gitignore
├── README.md                   (guide utilisateur)
├── pyproject.toml              (configuration build/dependencies)
└── requirements.txt            (dépendances pip)
```

## 🚀 Comment utiliser

### Via API Web
```bash
python scripts/run_api.py
# → http://127.0.0.1:8000
```

### Via CLI
```bash
python scripts/run_cli.py
```

### Importer le package
```python
from immo_agent.runIA import outil_dvf_historique, outil_dvf_estimation
from immo_agent.api import app
from immo_agent.main import chat_loop
```

## 📋 Organisation par rôle

| Dossier | Usage | Qui ? |
|---------|-------|-------|
| `immo_agent/` | Code métier | Développeurs |
| `scripts/` | Lancer l'app | Utilisateurs finaux |
| `frontend/` | Interface | Frontend dev |
| `data/` | BD, données | Données scientifique |
| `tests/` | Validation | QA / CI-CD |
| `config/` | Paramètres | DevOps / Config |
| `documentation/` | Spécs | Analystes |
| `exploration/` | Prototypage | Recherche |

## ✨ Avantages de cette structure

✅ **Clair** : chaque dossier a un rôle distinct
✅ **Scalable** : facile d'ajouter des modules
✅ **Professionnel** : suit les conventions Python
✅ **Maintenable** : organisation logique
✅ **Extensible** : prêt pour CI/CD et tests
