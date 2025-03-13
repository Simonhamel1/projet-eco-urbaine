import os
import pandas as pd

def charger_donnees(input_dir):
    fichier = os.path.join(input_dir, "data.csv")
    try:
        # Lire les données depuis le CSV
        donnees = pd.read_csv(fichier)
        print(f"Données chargées avec succès depuis {fichier}")
        return donnees
    except Exception as e:
        print(f"Erreur lors du chargement des données: {e}")
        return None

def analyser_donnees(data):
    # Exemple d'analyse : afficher les premières lignes
    print("Aperçu des données :")
    print(data.head())

def sauvegarder_resultats(output_dir, data):
    # Sauvegarde des résultats dans un nouveau fichier CSV
    fichier_out = os.path.join(output_dir, "resultats.csv")
    try:
        data.to_csv(fichier_out, index=False)
        print(f"Résultats sauvegardés dans {fichier_out}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des résultats: {e}")

def main():
    # Directories
    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    input_dir = os.path.join(root_dir, "input")
    output_dir = os.path.join(root_dir, "output")
    
    # Charger les données
    donnees = charger_donnees(input_dir)
    if donnees is None:
        return
    
    # Analyser les données
    analyser_donnees(donnees)
    
    # Traitement et création d'un nouveau DataFrame (exemple)
    resultats = donnees  # À remplacer par le code d'analyse réel
    
    # Sauvegarder les résultats
    sauvegarder_resultats(output_dir, resultats)

if __name__ == '__main__':
    main()