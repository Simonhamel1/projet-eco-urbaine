import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Charger les données (remplacer 'urbanisation_pib.csv' par votre fichier)
df = pd.read_csv('urbanisation.csv')

# Supprimer les valeurs manquantes
df = df.dropna(subset=['Urban_Pop_Pct', 'GDP_per_capita'])

# Transformation logarithmique des variables
df['log_Urbanisation'] = np.log(df['Urban_Pop_Pct'])
df['log_GDP_per_capita'] = np.log(df['GDP_per_capita'])

# Créer le scatter plot avec la droite de régression
plt.figure(figsize=(8, 6))
sns.regplot(x=df['log_Urbanisation'], y=df['log_GDP_per_capita'], scatter_kws={'alpha': 0.5})

# Ajouter des labels et un titre
plt.xlabel("log(Urbanisation %)")
plt.ylabel("log(PIB par habitant)")
plt.title("Relation entre Urbanisation et Croissance Économique")

# Afficher le graphique
plt.show()