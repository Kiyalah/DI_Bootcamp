l1 = ["7", "i", "i"]
l2 = ["T", "s", "x"]
l3 = ["h", "%", "?"]
l4 = ["i", " ", "#"]
l5 = ["s", "M", " "]
l6 = ["$", "a", " "]
l7 = ["#", "t", "%"]
l8 = ["^", "r", "!"]


matrix = [l1,l2,l3,l4,l5,l6,l7,l8]
secret_message = ""


for col in range(3):
    for row in range(8):
        if matrix[row][col].isalpha():
            secret_message += matrix[row][col]
            
print(secret_message)