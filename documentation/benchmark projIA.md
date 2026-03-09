# RAPPORT DE BENCHMARK - PROJET IMMOBILIER IA

## À remplir par le binôme

---

## 1. Informations générales

| | |
|:---|:---|
| **Titre du projet** | |
| **Binôme** | Étudiant 1 : <br> Étudiant 2 : |
| **Date** | |
| **Version** | 1.0 |

---

## 2. Objectif du benchmark

*En quelques lignes, expliquez pourquoi vous réalisez ce benchmark et ce que vous cherchez à évaluer.*

> Structurer notre exploration/veille sur les technologies a utiliser pour structurer notre choix de stack

---

## 3. Benchmark des agents / chatbots immobiliers existants

*Analysez au moins 3 solutions existantes (sites web, applications, assistants) qui proposent des services similaires à votre projet.*
Resp. Arnaud

### 3.1 Solution 1 : Joe AI

| Critère | Description |
|:---|:---|
| **Nom / Lien** | Joe AI (getjoe-ai.com) |
| **Type** | ☐ Site web ☐ Application mobile ☑ Chatbot ☑ Assistant vocal |
| **Fonctionnalités principales** | Qualification des leads, prise de rendez-vous, support administratif et technique, réponses instantanées 24/7 (téléphone, SMS, WhatsApp, mail). |
| **Sources de données utilisées** | Bases de données de l'agence (CRM, annonces immobilières, agendas). |
| **Technologies présumées** | LLM conversationnel, Speech-to-Text / Text-to-Speech pour la voix, intégrations API. |
| **Points forts** | Agent vocal très performant, automatisation poussée de la communication (appels entrants/sortants), intégration CRM fluide. |
| **Points faibles / limites** | Orienté principalement professionnels/agences (B2B), approche très transactionnelle, manque potentiellement d'outils analytiques visuels pour l'utilisateur. |
| **Ce que nous pourrions améliorer** | Proposer une interface utilisateur mixte (conversationnelle et visuelle) intégrant l'analyse de données de marché (DVF). |

### 3.2 Solution 2 : Keyzia

| Critère | Description |
|:---|:---|
| **Nom / Lien** | Keyzia (keyzia.fr) |
| **Type** | ☑ Site web ☐ Application mobile ☑ Chatbot ☐ Assistant vocal |
| **Fonctionnalités principales** | Cartographie interactive, estimation immobilière assistée par l'IA, centralisation des données (DPE, etc.), aide à la prospection foncière. |
| **Sources de données utilisées** | Open data immobilière (DVF, DPE, règles d'urbanisme, cadastre), plus de 1000 points de données par adresse. |
| **Technologies présumées** | IA d'analyse géospatiale, LLM, bases de données structurées et vectorielles. |
| **Points forts** | Très orienté data (open data, DVF), cartographie puissante, véritable outil d'aide à la décision immobilière. |
| **Points faibles / limites** | Outil d'analyse B2B complexe, moins orienté vers un dialogue simple et naturel pour un acheteur B2C. |
| **Ce que nous pourrions améliorer** | Allier cette richesse de données open-data (notamment DVF) à une interface purement conversationnelle (chatbot) très simple d'accès pour le grand public. |

### 3.3 Solution 3 : Livie

| Critère | Description |
|:---|:---|
| **Nom / Lien** | Livie (livie.info) |
| **Type** | ☐ Site web ☐ Application mobile ☑ Chatbot ☐ Assistant vocal |
| **Fonctionnalités principales** | Accueil des visiteurs sur site web, réponses aux FAQ, qualification des prospects, planification de visites, IA multilingue. |
| **Sources de données utilisées** | Données de l'agence (portefeuille de biens, agenda, FAQ interne). |
| **Technologies présumées** | LLM classique, RAG (Retrieval-Augmented Generation) sur les documents internes, intégration widget web. |
| **Points forts** | Très facile à intégrer sur un site web existant, disponible 24/7, personnalisable selon la marque de l'agence. |
| **Points faibles / limites** | Chatbot "classique" centré sur les biens en base, mais limité face à des requêtes immobilières métier plus poussées (ex: analyse de marché, estimation précise). |
| **Ce que nous pourrions améliorer** | Ajouter une vraie dimension d'estimation intelligente et d'analyse de marché en temps réel, plutôt que simplement de la réponse au client. |

*(Ajoutez autant de lignes que nécessaire)*

### 3.4 Synthèse du benchmark concurrentiel

*Quels sont les points communs entre ces solutions ? Quelles sont les lacunes du marché que votre projet pourrait combler ?*

**Points communs :**
- Ces solutions visent toutes à **automatiser la relation client** (qualification, prise de rendez-vous, support 24/7) dans le secteur immobilier.
- Elles s'adressent majoritairement aux **professionnels de l'immobilier** (agents, mandataires, syndics) dans une logique B2B pour leur faire gagner du temps.
- Elles s'appuient fortement sur l'intégration avec les bases de données privées des agences (CRM, portefeuilles de biens).

**Lacunes du marché & opportunités pour notre projet :**
- **Accès grand public aux données complexes :** Peu d'outils conversationnels simples permettent au grand public (B2C) d'interroger facilement des bases de données complexes comme les DVF (Demandes de Valeurs Foncières) de manière naturelle.
- **Croisement Analyse / Conversation :** Le marché est divisé entre les chatbots de relation client (Livie, Joe AI) et les outils cartographiques/analytiques lourds (Keyzia). Notre projet peut se démarquer en fusionnant les deux : un assistant naturel et fluide capable de fournir des insights data très précis (estimations basées sur des données open data).
- **Transparence de l'information :** Un agent IA conçu de zéro avec un modèle open-source, mettant en valeur l'open data gouvernementale, répond à un besoin de transparence du marché immobilier.

---

## 4. Benchmark des frameworks et outils d'orchestration IA

*Comparez les différentes options pour orchestrer votre agent IA.*
Resp.Fabien

### 4.1 LangChain

| Critère | Évaluation |
|:---|:---|
| **Documentation** | ☐ Excellente ☐ Bonne ☐ Moyenne ☐ Insuffisante |
| **Facilité de prise en main** | ☐ Très facile ☐ Facile ☐ Complexe ☐ Très complexe |
| **Support des outils (tools)** | ☐ Natif ☐ Via extensions ☐ Limité ☐ Non supporté |
| **Communauté / Écosystème** | ☐ Très active ☐ Active ☐ Peu active ☐ Inexistante |
| **Intégration avec les LLM** | ☐ Nombreuses ☐ Quelques-unes ☐ Limitées ☐ Aucune |
| **Documentation en français** | ☐ Oui, abondante ☐ Quelques ressources ☐ Très peu ☐ Aucune |
| **Notre avis / commentaires** | |

### 4.2 LangGraph

| Critère | Évaluation |
|:---|:---|
| **Documentation** | ☐ Excellente ☐ Bonne ☐ Moyenne ☐ Insuffisante |
| **Facilité de prise en main** | ☐ Très facile ☐ Facile ☐ Complexe ☐ Très complexe |
| **Support des outils (tools)** | ☐ Natif ☐ Via extensions ☐ Limité ☐ Non supporté |
| **Communauté / Écosystème** | ☐ Très active ☐ Active ☐ Peu active ☐ Inexistante |
| **Intégration avec les LLM** | ☐ Nombreuses ☐ Quelques-unes ☐ Limitées ☐ Aucune |
| **Documentation en français** | ☐ Oui, abondante ☐ Quelques ressources ☐ Très peu ☐ Aucune |
| **Notre avis / commentaires** | |

### 4.3 Orchestrateur maison

| Critère | Évaluation |
|:---|:---|
| **Documentation** | ☐ Excellente ☐ Bonne ☐ Moyenne ☐ Insuffisante |
| **Facilité de prise en main** | ☐ Très facile ☐ Facile ☐ Complexe ☐ Très complexe |
| **Support des outils (tools)** | ☐ Natif ☐ Via extensions ☐ Limité ☐ Non supporté |
| **Communauté / Écosystème** | ☐ Très active ☐ Active ☐ Peu active ☐ Inexistante |
| **Intégration avec les LLM** | ☐ Nombreuses ☐ Quelques-unes ☐ Limitées ☐ Aucune |
| **Documentation en français** | ☐ Oui, abondante ☐ Quelques ressources ☐ Très peu ☐ Aucune |
| **Notre avis / commentaires** | |

### 4.4 CrewAI

| Critère | Évaluation |
|:---|:---|
| **Documentation** | ☐ Excellente ☐ Bonne ☐ Moyenne ☐ Insuffisante |
| **Facilité de prise en main** | ☐ Très facile ☐ Facile ☐ Complexe ☐ Très complexe |
| **Support des outils (tools)** | ☐ Natif ☐ Via extensions ☐ Limité ☐ Non supporté |
| **Communauté / Écosystème** | ☐ Très active ☐ Active ☐ Peu active ☐ Inexistante |
| **Intégration avec les LLM** | ☐ Nombreuses ☐ Quelques-unes ☐ Limitées ☐ Aucune |
| **Documentation en français** | ☐ Oui, abondante ☐ Quelques ressources ☐ Très peu ☐ Aucune |
| **Notre avis / commentaires** | |

### 4.4 Synthèse et choix motivé

*Quel framework avez-vous choisi et pourquoi ?*

**Framework retenu :** 

**Justification :**




---

## 5. Benchmark des modèles de langage (LLM)

*Comparez les modèles que vous pourriez utiliser.* 
Resp.Fabien

| Critère | Mistral large | Qwen 8b | Gemini |
|:---|:---|:---|:---|
| **Fournisseur** | | | |
| **Type** | ☐ Open source ☐ Propriétaire | ☐ Open source ☐ Propriétaire | ☐ Open source ☐ Propriétaire |
| **Taille / Version** | | | |
| **Coût** | ☐ Gratuit ☐ Payant ☐ Freemium | ☐ Gratuit ☐ Payant ☐ Freemium | ☐ Gratuit ☐ Payant ☐ Freemium |
| **Performance / Qualité** | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne |
| **Vitesse d'inférence** | ☐ Rapide ☐ Moyenne ☐ Lente | ☐ Rapide ☐ Moyenne ☐ Lente | ☐ Rapide ☐ Moyenne ☐ Lente |
| **Support du français** | ☐ Excellent ☐ Bon ☐ Moyen ☐ Mauvais | ☐ Excellent ☐ Bon ☐ Moyen ☐ Mauvais | ☐ Excellent ☐ Bon ☐ Moyen ☐ Mauvais |
| **Facilité d'intégration** | ☐ Très facile ☐ Facile ☐ Complexe | ☐ Très facile ☐ Facile ☐ Complexe | ☐ Très facile ☐ Facile ☐ Complexe |
| **Limites (rate limits, etc.)** | | | |

**Choix du modèle retenu :** 

**Justification :**




---

## 6. Benchmark des bases de données

*Comparez les options pour stocker vos données.*
Resp.Arnaud

| Critère | PostgreSQL | MongoDB | PostgreSQL (avec pgvector) |
|:---|:---|:---|:---|
| **Type** | Relationnelle | | |
| **Support géospatial (PostGIS)** | ☐ Oui ☐ Non | ☐ Oui ☐ Non | ☐ Oui ☐ Non |
| **Performance** | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne |
| **Facilité d'installation** | ☐ Très facile ☐ Facile ☐ Complexe | ☐ Très facile ☐ Facile ☐ Complexe | ☐ Très facile ☐ Facile ☐ Complexe |
| **Documentation** | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne |
| **Communauté** | ☐ Très active ☐ Active ☐ Peu active | ☐ Très active ☐ Active ☐ Peu active | ☐ Très active ☐ Active ☐ Peu active |
| **Intégration avec Python** | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne |

**Choix de la base de données retenue :** 

**Justification :**




---

## 7. Benchmark des sources de données externes

*Évaluez les différentes sources de données que vous pourriez utiliser.*
Resp. Arnaud et Fabien

### 7.1 API DVF (Demandes de Valeurs Foncières)

| Critère | Évaluation |
|:---|:---|
| **URL / Accès** | https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/ |
| **Type d'accès** | ☐ API REST ☐ Téléchargement de fichiers ☐ Base de données ☐ Autre : |
| **Format des données** | ☐ JSON ☐ CSV ☐ XML ☐ Autre : |
| **Données disponibles** | |
| **Limitations (rate limit, volumétrie)** | |
| **Qualité des données** | ☐ Excellente ☐ Bonne ☐ Moyenne ☐ Mauvaise |
| **Mise à jour / Fraîcheur** | |
| **Documentation** | ☐ Excellente ☐ Bonne ☐ Moyenne ☐ Insuffisante |
| **Difficulté d'intégration** | ☐ Très facile ☐ Facile ☐ Complexe ☐ Très complexe |

### 7.2 Autre source 1 : [Nom]

| Critère | Évaluation |
|:---|:---|
| **URL / Accès** | |
| **Type d'accès** | ☐ API REST ☐ Téléchargement de fichiers ☐ Base de données ☐ Autre : |
| **Format des données** | ☐ JSON ☐ CSV ☐ XML ☐ Autre : |
| **Données disponibles** | |
| **Limitations (rate limit, volumétrie)** | |
| **Qualité des données** | ☐ Excellente ☐ Bonne ☐ Moyenne ☐ Mauvaise |
| **Mise à jour / Fraîcheur** | |
| **Documentation** | ☐ Excellente ☐ Bonne ☐ Moyenne ☐ Insuffisante |
| **Difficulté d'intégration** | ☐ Très facile ☐ Facile ☐ Complexe ☐ Très complexe |

### 7.3 Autre source 2 : [Nom]

| Critère | Évaluation |
|:---|:---|
| **URL / Accès** | |
| **Type d'accès** | ☐ API REST ☐ Téléchargement de fichiers ☐ Base de données ☐ Autre : |
| **Format des données** | ☐ JSON ☐ CSV ☐ XML ☐ Autre : |
| **Données disponibles** | |
| **Limitations (rate limit, volumétrie)** | |
| **Qualité des données** | ☐ Excellente ☐ Bonne ☐ Moyenne ☐ Mauvaise |
| **Mise à jour / Fraîcheur** | |
| **Documentation** | ☐ Excellente ☐ Bonne ☐ Moyenne ☐ Insuffisante |
| **Difficulté d'intégration** | ☐ Très facile ☐ Facile ☐ Complexe ☐ Très complexe |

### 7.4 Synthèse des sources retenues

| Source | Données utilisées | Méthode d'intégration | Priorité |
|:---|:---|:---|:---|
| DVF | | | ☐ Haute ☐ Moyenne ☐ Basse |
| | | | ☐ Haute ☐ Moyenne ☐ Basse |
| | | | ☐ Haute ☐ Moyenne ☐ Basse |

---

## 8. Benchmark des interfaces utilisateur / frontend

*Comparez les options pour créer l'interface de votre application.*
Resp.Fabien

| Critère | Streamlit | Gradio | FastAPI | Django|
|:---|:---|:---|:---|:---|
| **Rapidité de développement** | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne |
| **Composants chat intégrés** | ☐ Oui ☐ Non | ☐ Oui ☐ Non | ☐ Oui ☐ Non | ☐ Oui ☐ Non |
| **Personnalisation** | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne |
| **Documentation** | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne | ☐ Excellente ☐ Bonne ☐ Moyenne |
| **Communauté** | ☐ Très active ☐ Active ☐ Peu active | ☐ Très active ☐ Active ☐ Peu active | ☐ Très active ☐ Active ☐ Peu active | ☐ Très active ☐ Active ☐ Peu active |
| **Facilité de déploiement** | ☐ Très facile ☐ Facile ☐ Complexe | ☐ Très facile ☐ Facile ☐ Complexe | ☐ Très facile ☐ Facile ☐ Complexe | ☐ Très facile ☐ Facile ☐ Complexe |

**Choix de l'interface retenue :** 

**Justification :**




---

## 9. Synthèse générale du benchmark

### 9.1 Récapitulatif des choix technologiques

| Domaine | Technologie choisie |
|:---|:---|
| Framework d'orchestration IA | |
| Modèle de langage (LLM) | |
| Base de données | |
| Backend / API | |
| Frontend / Interface | |
| Sources de données externes | |

### 9.2 Justification globale

*Expliquez en quelques paragraphes pourquoi votre stack technologique est la plus adaptée au projet, compte tenu des contraintes (délai d'une semaine, compétences, objectifs).*




### 9.3 Enseignements clés du benchmark

*Qu'avez-vous appris en réalisant ce benchmark ? Quelles bonnes pratiques allez-vous adopter ?*




---

## 10. Annexes

*Liens vers les ressources consultées, articles, documentations, etc.*


