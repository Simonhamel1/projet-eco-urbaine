import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Charger les fichiers
pib_path = "pib.csv"
urbanisation_path = "urbanisation.csv"

# Lire les fichiers en sautant les 4 premières lignes de métadonnées
pib_df = pd.read_csv(pib_path, skiprows=4)
urbanisation_df = pd.read_csv(urbanisation_path, skiprows=4)

# Filtrer les indicateurs pertinents
pib_filtered = pib_df[pib_df["Indicator Code"] == "NY.GDP.PCAP.CD"].drop(columns=["Indicator Name", "Indicator Code"])
urbanisation_filtered = urbanisation_df[urbanisation_df["Indicator Code"] == "SP.URB.TOTL.IN.ZS"].drop(columns=["Indicator Name", "Indicator Code"])

# Transformer les données en format long
pib_melted = pib_filtered.melt(id_vars=["Country Name", "Country Code"], var_name="Année", value_name="PIB")
urbanisation_melted = urbanisation_filtered.melt(id_vars=["Country Name", "Country Code"], var_name="Année", value_name="Urbanisation")

# Convertir les années en nombres
pib_melted["Année"] = pd.to_numeric(pib_melted["Année"], errors="coerce")
urbanisation_melted["Année"] = pd.to_numeric(urbanisation_melted["Année"], errors="coerce")

# Fusionner les datasets sur le pays et l’année
merged_df = pd.merge(pib_melted, urbanisation_melted, on=["Country Name", "Country Code", "Année"], how="inner")
merged_df = merged_df.dropna()  # Supprimer les valeurs manquantes

# Appliquer la transformation logarithmique
merged_df["log(PIB)"] = np.log(merged_df["PIB"])
merged_df["log(Urbanisation)"] = np.log(merged_df["Urbanisation"])

# Tracer le graphique de dispersion avec régression linéaire
plt.figure(figsize=(8, 6))
sns.regplot(x="log(Urbanisation)", y="log(PIB)", data=merged_df, scatter_kws={'s': 10}, line_kws={"color": "black"})
plt.xlabel("log(Urbanisation)")
plt.ylabel("log(PIB par habitant)")
plt.title("Corrélation entre l'urbanisation et le PIB")
plt.show()

# Régression OLS
X = sm.add_constant(merged_df["log(Urbanisation)"])  # Ajouter une constante
y = merged_df["log(PIB)"]
model = sm.OLS(y, X).fit()

# Afficher le résumé des résultats
print(model.summary())