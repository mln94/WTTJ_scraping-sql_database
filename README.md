# Extracteur de Compétences pour Offres d'Emploi

## Description

Ce projet est un outil d'extraction automatique de compétences à partir d'offres d'emploi publiées sur Welcome to the Jungle. Il utilise web scraping pour collecter les descriptions de postes et l'API OpenAI pour analyser et extraire les compétences requises (techniques et non techniques).

## Fonctionnalités

- Scraping des offres d'emploi depuis Welcome to the Jungle
- Analyse et extraction des compétences via l'API OpenAI (GPT-4o-mini)
- Catégorisation des compétences en :
  - Compétences techniques (hard skills)
  - Compétences comportementales (soft skills)
  - Outils et technologies spécifiques
- Gestion des limites de l'API (rate limiting)
- Suivi de l'utilisation des tokens

## Prérequis

- Python 3.x
- Clé API OpenAI
- Fichier `.env` pour stocker la clé API
- Fichier `payload.json` pour les requêtes Algolia

## Installation

1. Cloner le dépôt
2. Installer les dépendances :
```bash
pip install requests beautifulsoup4 openai python-dotenv tiktoken
```
3. Créer un fichier `.env` à la racine du projet avec la clé API OpenAI :
```
OPENAI_API_KEY=votre_clé_api
```

## Utilisation

1. Préparer le fichier `payload.json` avec les paramètres de recherche Algolia
2. Exécuter le script principal :
```bash
python main.py
```

## Structure du Code

- `request_data()` : Initie les requêtes vers l'API Algolia de Welcome to the Jungle
- `get_job_url()` : Extrait les URLs des offres d'emploi
- `get_job_datas()` : Récupère les données des offres via web scraping
- `check_input_token_number()` : Vérifie et compte les tokens utilisés
- `send_to_openai()` : Envoie les données à l'API OpenAI pour extraction des compétences

## Format de Sortie

Les résultats sont retournés au format JSON avec la structure suivante :
```json
{
    "company_name": "Nom de l'entreprise",
    "job_title": "Titre du poste",
    "required_skills": {
        "soft_skills": ["Liste des soft skills"],
        "hard_skills": {
            "technical_skills": ["Liste des compétences techniques"],
            "tools": ["Liste des outils et technologies"]
        }
    }
}
```

## Limitations et Gestion des Requêtes

- Limitation à 3 requêtes avant pause de 2 minutes
- Pause de 2 minutes après 50 000 tokens utilisés (entrée + sortie)
- Délai de 5 secondes entre chaque scraping d'offre

## Améliorations Possibles

- Stockage des résultats dans une base de données
- Interface utilisateur pour visualiser les résultats
- Filtrage et recherche dans les compétences extraites
- Analyse statistique des compétences les plus demandées
