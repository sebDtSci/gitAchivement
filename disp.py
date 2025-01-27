import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Charger les accomplissements
def charger_accomplissements(fichier):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Générer une heatmap comme sur GitHub
def generer_calendrier_heatmap(fichier):
    # Charger les accomplissements
    accomplissements = charger_accomplissements(fichier)
    
    # Année courante
    annee = datetime.now().year
    premier_jour = datetime(annee, 1, 1)
    dernier_jour = datetime(annee, 12, 31)
    delta = (dernier_jour - premier_jour).days + 1

    # Créer une liste avec toutes les dates de l'année
    dates = [premier_jour + timedelta(days=i) for i in range(delta)]

    # Initialiser la grille pour 52 semaines x 7 jours (jours de la semaine)
    matrice = [[0 for _ in range(52)] for _ in range(7)]

    # Remplir la matrice avec les accomplissements
    for date in dates:
        jour_semaine = date.weekday()  # 0 = lundi, 6 = dimanche
        semaine = date.isocalendar()[1] - 1  # Numéro de la semaine
        cle_date = date.strftime("%Y-%m-%d")
        accomplissement = accomplissements.get(cle_date, 0)

        # Convertir en entier si nécessaire (par ex., si c'est une liste ou une chaîne)
        if isinstance(accomplissement, list):
            accomplissement = len(accomplissement)  # Par exemple, longueur de la liste
        elif isinstance(accomplissement, str):
            try:
                accomplissement = int(accomplissement)  # Tenter de convertir en entier
            except ValueError:
                accomplissement = 0  # Ignorer si ce n'est pas un nombre valide

        matrice[jour_semaine][semaine] += accomplissement  # Ajouter l'accomplissement

    # Visualisation
    plt.figure(figsize=(15, 5))
    plt.imshow(matrice, cmap="Greens", aspect="auto", interpolation="nearest")
    plt.colorbar(label="Nombre d'accomplissements")
    plt.title(f"Calendrier des accomplissements - {annee}")
    plt.xlabel("Semaines")
    plt.ylabel("Jours de la semaine")
    plt.yticks(range(7), ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"])
    plt.show()

if __name__ == "__main__":
    FICHIER = "accomplissements.json"
    generer_calendrier_heatmap(FICHIER)