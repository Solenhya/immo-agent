# 🚀 Guide de démarrage - immo-agent

## Installation rapide

```bash
# 1. Cloner et entrer dans le projet
git clone https://github.com/Arno37/immo-agent.git
cd immo-agent

# 2. Configurer l'environnement
cp .env.example .env
# Éditer .env avec ta clé MISTRAL_API_KEY

# 3. Installer les dépendances
pip install -r requirements.txt
# ou pour dev : pip install -e ".[dev]"
```

## 🎯 Utiliser le projet

### Option 1️⃣ : API Web (Recommandé)
```bash
python scripts/run_api.py
```
Puis ouvrez : **http://127.0.0.1:8000**

### Option 2️⃣ : CLI interactive
```bash
python scripts/run_cli.py
```

### Option 3️⃣ : Importer comme module Python
```python
from immo_agent.runIA import outil_dvf_estimation

# Estimer un bien
estimation = outil_dvf_estimation(
    ville="Paris",
    surface="120",
    type_bien="Maison",
    etat="bon"
)
print(estimation)
```

## 📁 Architecture du projet

**Voir [STRUCTURE.md](STRUCTURE.md)** pour la description complète

Dossiers clés :
- 📦 **immo_agent/** → Code source (développeurs)
- 🎯 **scripts/** → Points d'entrée (utilisateurs)
- 🎨 **frontend/** → Interface web
- 📊 **data/** → Bases de données
- 🧪 **tests/** → Tests unitaires

## ⚙️ Configuration

Les paramètres se trouvent dans 2 fichiers :

1. **`.env`** (secrets)
   ```
   MISTRAL_API_KEY=sk_...
   GROQ_API_KEY=gsk_...
   ```

2. **`config/settings.py`** (paramètres publics)
   ```python
   DB_PATH = "data/immo_ventes.db"
   API_PORT = 8000
   DEFAULT_MODEL = "mistral-large-latest"
   ```

## ✅ Vérifier l'installation

```bash
python immo_agent/check_setup.py
```

## 🧪 Lancer les tests

```bash
pytest tests/
# ou avec couverture : pytest --cov=immo_agent tests/
```

## 📚 Documentation

- [STRUCTURE.md](STRUCTURE.md) - Organisation du projet
- [README.md](README.md) - Description générale
- [documentation/](documentation/) - Spécifications détaillées

## 🐛 Troubleshooting

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError: immo_agent` | Installer avec `pip install -e .` |
| Port 8000 occupé | `python scripts/run_api.py --port 8001` |
| Clé API manquante | Créer `.env` avec `MISTRAL_API_KEY=...` |
| BD non trouvée | Lancer `python immo_agent/csv_to_sqlite.py` |

## 💡 Développement

```bash
# Format le code
black immo_agent/

# Vérifier les types
mypy immo_agent/

# Lint
flake8 immo_agent/

# Développement en mode auto-reload
python scripts/run_api.py  # reload=True par défaut
```

## 📦 Structure recommandée pour ajouter du code

```python
# immo_agent/features/ma_feature.py
from immo_agent.runIA import model
from config import DB_PATH

def ma_fonction():
    """Ma nouvelle fonction bien organisée."""
    pass
```

Puis importer :
```python
from immo_agent.features import ma_fonction
```

---

**Besoin d'aide ?** Consultez [STRUCTURE.md](STRUCTURE.md) ou les docstrings du code.
