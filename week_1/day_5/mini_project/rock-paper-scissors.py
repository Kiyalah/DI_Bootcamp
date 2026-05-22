# Importer la classe Game depuis game.py
from game import Game


# Fonction pour afficher le menu
def get_user_menu_choice():

    print("\n--- MENU ---")
    print("(P) Play a new game")
    print("(S) Show scores")
    print("(Q) Quit")

    # Demander le choix utilisateur
    choice = input("Enter your choice: ").lower()

    # Vérifier la saisie
    if choice in ["p", "s", "q"]:
        return choice

    print("Invalid choice.")
    return None


# Fonction pour afficher les résultats
def print_results(results):

    print("\n--- GAME RESULTS ---")

    print(f"Wins   : {results['win']}")
    print(f"Losses : {results['loss']}")
    print(f"Draws  : {results['draw']}")

    print("\nThanks for playing!")


# Fonction principale
def main():

    # Dictionnaire pour stocker les scores
    results = {
        "win": 0,
        "loss": 0,
        "draw": 0
    }

    # Boucle principale du programme
    while True:

        user_choice = get_user_menu_choice()

        # Jouer une partie
        if user_choice == "p":

            # Créer un objet Game
            game = Game()

            # Jouer et récupérer le résultat
            result = game.play()

            # Ajouter le résultat dans le dictionnaire
            results[result] += 1


        # Afficher les scores
        elif user_choice == "s":

            print_results(results)


        # Quitter le programme
        elif user_choice == "q":

            print_results(results)

            break


# Lancer le programme
main()