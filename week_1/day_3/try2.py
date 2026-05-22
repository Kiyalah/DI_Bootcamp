class Cat:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def oldest_cat(cat1, cat2, cat3):
        return max((cat1, cat2, cat3), key=lambda c: c.age)
    
    
cat1= Cat("Aziz",3)
cat2= Cat("Mimi",5)
cat3= Cat("Kiki",2)

oldest= Cat.oldest_cat(cat1,cat2,cat3)
print(f"The oldest cat is: {oldest.name} with {oldest.age} years.")

