number = int(input("Enter a number: "))
length = int(input("Enter a length: "))

mult = []

for i in range(1, length + 1):
	mult.append(number * i)

print(mult)
	
