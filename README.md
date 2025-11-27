# Dashboard E-commerce

> Dashboard interactif pour visualiser les ventes et les clients, construit avec **Streamlit** et **Supabase**.

---

## Badges

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://dashboard-e-commerce-arditop.streamlit.app/)  
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)

---

## Description

Ce projet permet de :

- Visualiser les ventes par catégorie et dans le temps.
- Suivre les indicateurs clés : chiffre d’affaires, panier moyen, produit le plus vendu.
- Analyser les clients par âge, genre et région.
- Gérer l’authentification avec Supabase (connexion, création de compte, sessions).

---

## Captures d’écran

### Page Ventes
<img width="1325" height="850" alt="pages ventes" src="https://github.com/user-attachments/assets/4b60ad18-2a65-4a5d-82e2-c184bdedfbee" />

### Page Clients
<img width="1325" height="857" alt="pages clients" src="https://github.com/user-attachments/assets/4d404f07-1065-4f59-aafc-baf432f7bc42" />

### Page Analyses

<img width="1333" height="862" alt="page analyses" src="https://github.com/user-attachments/assets/e6304c43-e588-4eb2-ab85-cc43918fc6bb" />


---

## Technologies utilisées

- [Python 3.13](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Supabase](https://supabase.com)
- [Plotly](https://plotly.com/python/)
- [DuckDB / Pandas](https://duckdb.org/)


### Description rapide des dossiers et fichiers :

- **main.py** : point d’entrée principal de l’application.
- **pages/** : contient les pages secondaires de l’app :
  - `ventes.py` : page des ventes et KPIs.
  - `clients.py` : page analyse clients.
  - `analyses.py` : analyses régionales et autres métriques.
- **utils/** : fonctions utilitaires partagées :
  - `auth_supabase.py` : gestion de l’authentification via Supabase.
  - `charts.py` : fonctions de visualisation.
  - `data_loader.py` : chargement des données.
  - `metrics.py` : calcul des métriques clés (CA, panier moyen…).
- **data/** : fichiers CSV ou bases de données locales.
- **README.md** : documentation du projet.
