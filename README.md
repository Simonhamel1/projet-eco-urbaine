# Projet Eco-Urbaine : Urbanisation et Croissance Économique

## Description

Ce projet explore la relation entre l'urbanisation et la croissance économique, notamment à travers l'analyse de données émises par la Banque mondiale et d'autres sources institutionnelles. L'objectif est de comprendre comment la population concentrée dans les villes influence le PIB et quels facteurs, tels que l'éducation, renforcent ou modèrent cette relation.

## Structure du Projet

Le workspace est organisé de la manière suivante :

- **recherche/**  
  - **code/** : Contient des scripts Python (`urban.py`, `urban2.py`) et des fichiers de données (CSV) utilisés pour l'analyse des indicateurs (croissance du PIB, urbanisation, etc.).
  - **partie code,input,output/** : Regroupe les notebooks Jupyter (`main.ipynb`, `test.ipynb`) et scripts Python qui traitent, nettoient et visualisent les données.
  - **partie ressource/** : Comprend les documents de présentation, le plan de l'exposé, les références bibliographiques et d'autres ressources utiles.
- **renduFinal/**  
  - **do/** : Notebooks et scripts d'analyse finale.
  - **inputs/** et **outputs/** : Dossiers dédiés aux fichiers sources et aux résultats (graphes, rapports, etc.).

## Prérequis

- **Python 3.7+**
- Bibliothèques Python :
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - statsmodels
  - geopandas
  - requests, zipfile, py7zr

## Installation

1. Clonez le repository :
   ```sh
   git clone https://github.com/votre-utilisateur/projet-eco-urbaine.git
   ```
2. Installez les dépendances (vous pouvez utiliser `requirements.txt` si disponible) :
   ```sh
   pip install -r pandas numpy matplotlib seaborn statsmodels geopandas requests zipfile py7zr
   ```

## Utilisation

### Analyse des données

- **Notebooks d'analyse**  
  Les notebooks dans `recherche/partie code,input,output/` et `renduFinal/do/` contiennent l'ensemble des analyses réalisées (nettoyage des données, régressions, visualisations, etc.).  
  Pour lancer un notebook, utilisez Jupyter ou VS Code avec le support des notebooks.

- **Scripts Python**  
  Les scripts (`main.py`, `urban.py`, etc.) vous permettent de charger, traiter et analyser les données automatiquement.  
  Par exemple, pour exécuter le script principal :
  ```sh
  python recherche/partie\ code,input,output/code/main.py
  ```

### Structure des données

- Les fichiers CSV contenus dans les dossiers `inputs/` et `recherche/code/` contiennent les données brutes issues d'organismes tels que la Banque mondiale et l'INSEE.
- Les résultats et graphiques finaux se trouvent dans les dossiers `outputs/` et `renduFinal/outputs/`.

## Documentation et Ressources

- Le dossier **partie ressource/** contient la planification de l'exposé, les bibliographies ainsi que des liens importants (ex. [Banque mondiale](https://data.worldbank.org/indicator/SP.URB.TOTL.IN.ZS)).
- Veuillez consulter les notebooks et scripts pour plus de détails sur les méthodes d'analyse réalisées.

## Auteurs

- Hamelin Simon, Balde-Cisse Ibrahima, Marmelat Paul, Pupier Charly
