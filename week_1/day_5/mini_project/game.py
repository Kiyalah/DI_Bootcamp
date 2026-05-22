# Importer random pour permettre à l'ordinateur
# de choisir un élément aléatoire
import random


class Game:

    # Demander à l'utilisateur de choisir rock/paper/scissors
    def get_user_item(self):

        # Boucle jusqu'à ce que l'utilisateur entre une bonne valeur
        while True:

            user_choice = input(
                "Choose rock (r), paper (p) or scissors (s): "
            ).lower()

            # Vérification de la saisie
            if user_choice in ["rock", "paper", "scissors", "r", "p", "s"]:
                # Mapper les choix abrégés vers les choix complets
                if user_choice == "r" or user_choice == "rock":
                    return "rock"
                elif user_choice == "p" or user_choice == "paper":
                    return "paper"
                elif user_choice == "s" or user_choice == "scissors":
                    return "scissors"

            print("Invalid choice. Try again.")


    # L'ordinateur choisit un élément aléatoire
    def get_computer_item(self):

        items = ["rock", "paper", "scissors"]

        # random.choice choisit un élément au hasard
        computer_choice = random.choice(items)

        return computer_choice


    # Déterminer le résultat du jeu
    def get_game_result(self, user_item, computer_item):

        # Cas d'égalité
        if user_item == computer_item:
            return "draw"

        # Cas où le joueur gagne
        elif (
            (user_item == "rock" and computer_item == "scissors")
            or
            (user_item == "paper" and computer_item == "rock")
            or
            (user_item == "scissors" and computer_item == "paper")
        ):
            return "win"

        # Sinon le joueur perd
        else:
            return "loss"


    # Fonction principale pour jouer une partie
    def play(self):

        # Récupérer le choix du joueur
        user_item = self.get_user_item()

        # Récupérer le choix de l'ordinateur
        computer_item = self.get_computer_item()

        # Déterminer le résultat
        result = self.get_game_result(
            user_item,
            computer_item
        )

        # Afficher le résultat
        print(
            f"\nYou selected {user_item}. "
            f"The computer selected {computer_item}."
        )

        # Message selon le résultat
        if result == "win":
            print("You win!")

        elif result == "loss":
            print("You lose!")

        else:
            print("It's a draw!")

        # Retourner le résultat
        return result