import argparse
import json
from datetime import datetime
from disp import generer_calendrier_heatmap

# Fichier de stockage
FICHIER = "accomplissements.json"

# Ajouter un accomplissement
def ajouter_accomplissement(fichier, titre, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            journal = json.load(f)
    except FileNotFoundError:
        journal = {}

    # Ajouter le titre à la date
    if date not in journal:
        journal[date] = []
    journal[date].append(titre)
    
    # Sauvegarder dans le fichier
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(journal, f, indent=4)
    
    print(f"Accomplissement ajouté : [{date}] {titre}")

# Afficher le contenu du journal
def afficher_journal(fichier):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            journal = json.load(f)
        for date, titres in journal.items():
            print(f"{date}:")
            for titre in titres:
                print(f"  - {titre}")
    except FileNotFoundError:
        print("Aucun journal trouvé. Ajoutez des accomplissements pour commencer.")

# Configurer les arguments de la ligne de commande
def main():
    parser = argparse.ArgumentParser(description="Suivi des accomplissements quotidiens.")
    subparsers = parser.add_subparsers(dest="commande", help="Commandes disponibles")
    
    # Commande pour ajouter un accomplissement
    parser_add = subparsers.add_parser("add", help="Ajouter un accomplissement")
    parser_add.add_argument("titre", type=str, help="Titre de l'accomplissement")
    parser_add.add_argument("--date", type=str, help="Date au format YYYY-MM-DD (par défaut : aujourd'hui)")
    
    # Commande pour afficher le journal
    parser_show = subparsers.add_parser("show", help="Afficher le journal des accomplissements")

    # Commande pour afficher le calendrier
    parser_display = subparsers.add_parser("display", help="Afficher le journal des accomplissements visuellement")
    
    # Analyse des arguments
    args = parser.parse_args()
    
    if args.commande == "add":
        ajouter_accomplissement(FICHIER, args.titre, args.date)
    elif args.commande == "show":
        afficher_journal(FICHIER)
    elif args.commande == "display":
        generer_calendrier_heatmap(FICHIER)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()