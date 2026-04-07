# NOTE DE CADRAGE - PROJET IMMOBILIER IA

## À remplir par le binôme

---

## 1. Informations générales

| | |
|:---|:---|
| **Titre du projet** | |
| **Binôme** | Étudiant 1 : <br> Étudiant 2 : |
| **Date de début** | |
| **Date de livraison** | |
| **Lien dépôt GitHub** | |

---

## 2. Présentation du projet

### 2.1 Objectif principal (en une phrase)

> Creer un agent IA pour guider un utilisateur dans ses démarche immobiliere

### 2.2 Problématique / besoin utilisateur

*Quel problème concret l'application va-t-elle résoudre ? Centraliser des outils (prévision immobiliere etc) Dans un outils interactif et adaptatif. Pour quel type d'utilisateur ? Pour tout utilisateur qui a des questions immobilière




### 2.3 Périmètre fonctionnel

*Cochez les fonctionnalités que vous prévoyez d'implémenter :*

- [x] Interface de chat / conversation
- [x] Recherche de biens immobiliers par critères
- [x] Estimation de prix à partir des données DVF
- [?] Informations sur une commune (écoles, transports, commerces)
- [?] Conseils personnalisés (investissement, achat, location)
- [x] Historique des conversations
- [?] Autre (précisez) : 
Suivi utilisateur (summarization des conversations pour avoir un profil)
---

## 3. Architecture technique

### 3.1 Stack technologique choisie

| Composant | Technologie retenue | Justification |
|:---|:---|:---|
| Framework IA / Orchestration | | |
| Modèle de langage (LLM) | | |
| Base de données | | |
| Backend / API | | |
| Frontend / Interface | | |
| Hébergement / Déploiement | | |
| Versionnement | Git + GitHub | |

### 3.2 Sources de données externes

*Listez les APIs ou jeux de données que vous allez utiliser :*

| Source | Données récupérées | Méthode d'accès (API directe, fichier, etc.) |
|:---|:---|:---|
| data.gouv.fr / DVF | | |
| | | |
| | | |

### 3.3 Outils / fonctions que l'agent pourra utiliser

*Décrivez les "tools" que vous allez implémenter pour que l'agent interagisse avec le monde extérieur :*

| Nom de l'outil | Description | Source de données associée |
|:---|:---|:---|
| Ex: rechercher_prix_moyen | Calcule le prix moyen au m² dans une commune | Base PostgreSQL (données DVF) |
| | | |
| | | |
| | | |

---

## 4. Modélisation des données

### 4.1 Structure de la base de données

*Décrivez les principales tables que vous allez créer dans PostgreSQL :*

**Table 1 :** 
- Colonnes :
- Clé primaire :
- Relations :

**Table 2 :** 
- Colonnes :
- Clé primaire :
- Relations :

*(Ajoutez autant de tables que nécessaire)*

### 4.2 Schéma relationnel (optionnel)

*Si vous avez un schéma, vous pouvez le décrire ou l'inclure en lien :*



---

## 5. Organisation et répartition du travail

### 5.1 Répartition des rôles

| Étudiant | Responsabilités principales |
|:---|:---|
| Arnaud | |
| Fabien |"Scrum Master"|
A décider "product owner" (responsable de l'intégrité du produit)

### 5.2 Planification prévisionnelle

| Jour | Objectifs | Tâches détaillées | Responsable |
|:---|:---|:---|:---|
| Lundi | Initialisation | | Fabien|
| Mardi | Développement | | |
| Mercredi | **Jalon mi-parcours** | | |
| Jeudi | Intégration | | |
| Vendredi | Finalisation | | |

### 5.3 Outils de gestion de projet utilisés

- [x] GitHub Projects
- [ ] Trello / Notion
- [ ] Autre : 

---

## 6. Contraintes et risques identifiés

### 6.1 Contraintes techniques

*Limitations connues (API rate limits, taille des données, temps de réponse, etc.) :*



### 6.2 Risques et plans de contournement

| Risque | Probabilité (Faible/Moyenne/Élevée) | Impact | Plan B / Mitigation |
|:---|:---|:---|:---|
| API DVF indisponible | | | |
| Temps de réponse trop long | | | |
| Difficulté d'intégration du LLM | | | |
| | | | |

---

## 7. Sources de données - Évaluation

### 7.1 API DVF (Demandes de Valeurs Foncières)

| Critère | Évaluation |
|:---|:---|
| **URL / Accès** | https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/ |
| **Type d'accès** | ☑️ Téléchargement de fichiers |
| **Format des données** | ☑️ CSV |
| **Données disponibles** | Historique complet des transactions immobilières en France : prix, surface, type de bien, localisation, date de mutation, etc. |
| **Limitations** | Mise à jour mensuelle/trimestrielle ; données anonymisées ; ~2-3 mois de délai avant intégration |
| **Qualité des données** | ☑️ Excellente - Source officielle (DGFIP) |
| **Mise à jour / Fraîcheur** | Données actualisées tous les 1-2 mois ; dernière mise à jour 2025 S1 |
| **Documentation** | ☑️ Excellente - Dictionnaire complet et guides d'utilisation fournis |
| **Difficulté d'intégration** | ☑️ Facile - CSV standardisé, importable directement en SQLite |

### 7.2 Autre source 1 : API Communes (geo.api.gouv.fr)

| Critère | Évaluation |
|:---|:---|
| **URL / Accès** | https://geo.api.gouv.fr |
| **Type d'accès** | ☑️ API REST |
| **Format des données** | ☑️ JSON |
| **Données disponibles** | Population, géolocalisation, code postal, région, département de chaque commune française |
| **Limitations** | Pas de rate limit documenté ; réponses rapides (<100ms) |
| **Qualité des données** | ☑️ Excellente - Source officielle INSEE |
| **Mise à jour / Fraîcheur** | Mise à jour annuelle ; données 2024 actuelles |
| **Documentation** | ☑️ Excellente - API simple et bien documentée |
| **Difficulté d'intégration** | ☑️ Très facile - Appels REST directs, pas d'authentification |

### 7.3 Autre source 2 : [À déterminer - Météo / Transports / Commerces]

| Critère | Évaluation |
|:---|:---|
| **URL / Accès** | À définir selon besoin futur |
| **Type d'accès** | ☐ API REST ☐ Téléchargement ☐ Base de données ☐ Autre |
| **Format des données** | À définir |
| **Données disponibles** | Compléments potentiels : données météo, réseau transport, commerces proches |
| **Limitations** | À évaluer |
| **Qualité des données** | À évaluer |
| **Mise à jour / Fraîcheur** | À évaluer |
| **Documentation** | À évaluer |
| **Difficulté d'intégration** | À évaluer |

### 7.4 Synthèse des sources retenues

| Source | Données utilisées | Méthode d'intégration | Priorité |
|:---|:---|:---|:---|
| **DVF** | Prix au m², historique ventes, types bien | Import CSV → SQLite (`csv_to_sqlite.py`) | ☑️ **Haute** |
| **API Communes** | Population, géolocalisation | Appels API REST directs (outil `outil_infos_ville`) | ☑️ **Haute** |
| **Métadonnées** | Données utilisateur, historique conversations | SQLite (sessions, memory.db) | ☑️ **Haute** |

---

## 8. Critères de succès

### 8.1 Minimum Viable Product (MVP)

*Ce que vous considérez comme le "minimum acceptable" pour vendredi :*

- [ ] Chat fonctionnel
- [ ] Agent dispose outil estimation
- [ ] Agent utilise outil estimation
- [ ] Interface utilisateur

### 8.2 Fonctionnalités "nice to have" (si temps)

- [ ] Autres outils : MCP gouv, 
- [ ] Enregistrement conversation
- [ ] Creation profil utilisateur avec summarization
- [ ] Recherche de bien immobilier
- [ ] 

---

## 9. Validation

| | Nom | Date | Signature |
|:---|:---|:---|:---|
| **Arnaud** | | | |
| **Fabien** | | | |
| **Formateur (optionnel)** | | | |

---

## 10. Annexes

*Liens utiles, ressources, documentation, etc.*


