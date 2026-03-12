# 🏠 Solenhya Immo Agent

Agent IA pour estimer les biens immobiliers, consulter l'historique des ventes (DvF) et trouver des biens similaires.

## 📋 Prérequis

- Python 3.9+
- Clé API Groq (gratuite sur [console.groq.com](https://console.groq.com))

## 🚀 Installation

```bash
# 1. Cloner le repo
git clone https://github.com/Arno37/immo-agent.git
cd immo-agent

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer l'API Key
cp .env.example .env
# Éditer .env et ajouter ta clé GROQ_API_KEY
```

## ⚙️ Configuration (.env)

Crée un fichier `.env` dans la racine du projet :

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

Obtiens ta clé gratuite : https://console.groq.com/keys

## 🎯 Utilisation

### Via Web UI (Recommandé)

```bash
python3 api.py
```

Puis accède à : `http://127.0.0.1:8000`

### Via CLI

```bash
python3 main.py
```

L'agent support les demandes comme :
- "Quelle est l'estimation d'une maison de 120m² à Paris ?"
- "Quel est l'historique des ventes d'appartements à Lyon ?"
- "Quels sont les biens similaires à Marseille ?"
- "Quelle est la population de Nice ?"

## 📊 Données

- Base de données DVF (Valeurs Foncières) : `data/immo_ventes.db`
- Source : Données immobilières officielles françaises

## 🛠️ Architecture

```
immo-agent/
├── runIA.py          # Définition des outils IA (DVF, estimations)
├── api.py            # API FastAPI web
├── main.py           # CLI chat (WIP - dépendances manquantes)
├── frontend/         # Interface web React
├── data/
│   └── immo_ventes.db  # Base de données SQLite
└── requirements.txt  # Dépendances Python
```

## 🚦 État du projet

- ✅ Outils DVF fonctionnels
- ✅ API web FastAPI
- ✅ Interface web (HTML/CSS/JS)
- ⏳ CLI chat (langgraph/mcp à installer)

## 📝 Exemples de requêtes

```
"Estime une maison de 150m² à Saint-Tropez en bon état"
→ Résultat : Estimation basée sur les ventes DVF locales

"Montre-moi les ventes récentes d'appartements à Paris"
→ Résultat : Historique des prix au m² et ventes

"Quelle est la population de Cannes ?"
→ Résultat : Données INSEE officielles
```

## 🐛 Troubleshooting

**ModuleNotFoundError: langchain_groq**
```bash
pip install -r requirements.txt
```

**GROQ_API_KEY not found**
```bash
echo "GROQ_API_KEY=gsk_..." > .env
```

**Port 8000 déjà utilisé**
```bash
python3 -c "import os; os.environ['PORT']='8001'; exec(open('api.py').read())"
```

## 📄 Licence

MIT
