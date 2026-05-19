word = input("Entrez un mot : ")

result = ""

for letter in word:
    if result == "" or letter != result[-1]:
        result += letter

print(result)