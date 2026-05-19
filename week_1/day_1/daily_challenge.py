# Challenge 1


# Ask the user for a number and a length.
# Create a program that prints a list of multiples of the number until the list length reaches length.
# Examples


# number: 7 - length 5 ➞ [7, 14, 21, 28, 35]

# number: 12 - length 10 ➞ [12, 24, 36, 48, 60, 72, 84, 96, 108, 120]

# number: 17 - length 6 ➞ [17, 34, 51, 68, 85, 102]

while True:
    try:
        number = int(input("Entrez le nombre (entier) : ").strip())
        break
    except ValueError:
        print("Entrée invalide — veuillez entrer un entier.")

while True:
    try:
        length = int(input("Entrez la longueur (entier >= 0) : ").strip())
        if length < 0:
            print("La longueur doit être >= 0.")
            continue
        break
    except ValueError:
        print("Entrée invalide — veuillez entrer un entier.")


multiples = []
for i in range(1, length + 1):
    multiples.append(number * i)

print(multiples)


# Challenge 2


# Write a program that asks a string to the user, and display a new string with any duplicate consecutive letters removed.

# Examples



# user's word : "ppoeemm" ➞ "poem"

# user's word : "wiiiinnnnd" ➞ "wind"

# user's word : "ttiiitllleeee" ➞ "title"

# user's word : "cccccaaarrrbbonnnnn" ➞ "carbon"


# Notes
# Final strings won’t include words with double letters (e.g. “passing”, “lottery”).
word = input("Entrez un mot : ")

result = ""

for letter in word:
    if result == "" or letter != result[-1]:
        result += letter

print(result)
