# Défi 1 : Dictionnaire d’index des lettres
# Objectif : Créer un dictionnaire qui stocke les indices (numéro de position) de chaque lettre d'un mot fourni par l'utilisateur (input()).



# Principaux sujets en Python :

# Saisie utilisateur ( input())
# Dictionnaires
# Boucles ( forboucle)
# Instructions conditionnelles ( if, else)
# Manipulation de chaînes
# Listes


# Instructions:
# 1. Saisie de l'utilisateur :

# Demandez à l'utilisateur de saisir un mot.
# Stockez le mot saisi dans une variable.
# 2. Création du dictionnaire :

# Parcourez chaque caractère du mot saisi à l'aide d'une boucle.
# Vérifiez ensuite si le caractère est déjà une clé du dictionnaire.

#     * If it is, append the current index to the list associated with that key.
#     * If it is not, create a new key-value pair in the dictionary.
# Assurez-vous que les caractères (clés) sont des chaînes de caractères.
# Assurez-vous que les indices (valeurs) sont stockés dans des listes.
# 3. Résultat attendu :

# Pour l’entrée « dodo », la sortie devrait être : {"d": [0, 2], "o": [1, 3]}.
# Pour l'entrée « froggy », la sortie devrait être : {"f": [0], "r": [1], "o": [2], "g": [3, 4], "y": [5]}.
# Pour l’entrée « raisins », la sortie devrait être : {"g": [0], "r": [1], "a": [2], "p": [3], "e": [4], "s": [5]}.

word = input("Enter a word: ")

letters_dict = {}

for index, letter in enumerate(word):

    if letter in letters_dict:
        letters_dict[letter].append(index)

    else:
        letters_dict[letter] = [index]

print(letters_dict)





# Défi 2 : Articles abordables
# Objectif : Créer un programme qui imprime une liste d'articles pouvant être achetés avec une somme d'argent donnée.



# Principaux sujets en Python :

# Dictionnaires
# Boucles ( forboucle)
# Instructions conditionnelles ( if, else)
# Manipulation de chaînes de caractères ( replace())
# Conversion de type ( int())
# Listes
# Tri ( sorted())


# Instructions:
# 1. Stocker les données :

# Vous recevrez un dictionnaire ( items_purchase) où les clés sont les noms des articles et les valeurs leurs prix (sous forme de chaînes de caractères suivies du symbole dollar). La priorité est définie par la position de l'article dans le dictionnaire : du plus important au moins important.
# Vous recevrez également une chaîne de caractères ( wallet) représentant le montant d'argent dont vous disposez.
# 2. Nettoyage des données :

# Vous devez supprimer le signe dollar et les virgules à l'aide de Python. Ne les codez pas en dur.
# 3. Déterminer les articles abordables :

# Créez une liste basketet ajoutez-y les articles que vous pouvez acheter avec l'argent que vous avez dans votre portefeuille.
# N'oubliez pas de mettre à jour votre portefeuille après avoir acheté un article.
# Si la liste basketest vide (aucun article ne peut être acheté), renvoyez la chaîne « Rien ».
# Sinon, imprimez la basketliste par ordre alphabétique.
# 4. Exemples :

# Donné:
# items_purchase = {"Water": "$1", "Bread": "$3", "TV": "$1,000", "Fertilizer": "$20"}
# wallet = "$300"


# Le résultat devrait être : ["Bread", "Fertilizer", "Water"].

# Donné:
# items_purchase = {"Apple": "$4", "Honey": "$3", "Fan": "$14", "Bananas": "$4", "Pan": "$100", "Spoon": "$2"}
# wallet = "$100"


# Le résultat devrait être : ["Apple", "Bananas", "Fan", "Honey", "Spoon"].

# Donné:
# items_purchase = {"Phone": "$999", "Speakers": "$300", "Laptop": "$5,000", "PC": "$1200"}
# wallet = "$1"


# Le résultat devrait être : "Nothing".



items_purchase = {
    "Water": "$1",
    "Bread": "$3",
    "TV": "$1,000",
    "Fertilizer": "$20"
}

wallet = "$300"

wallet_value = int(wallet.replace("$", "").replace(",", ""))

basket = []

# Loop through the dictionary
for item, price in items_purchase.items():

    # Clean and convert the price
    price_value = int(price.replace("$", "").replace(",", ""))

    # Check if the item is affordable
    if price_value <= wallet_value:

        # Add item to basket
        basket.append(item)

        # Update wallet
        wallet_value -= price_value

# Final result
if len(basket) == 0:
    print("Nothing")

else:
    print(sorted(basket))

