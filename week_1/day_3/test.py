# class Zoo:
#     def __init__(self, name):
#         self.name = name
#         self.animals = []
        
#     def add_animal(self, new_animal):
#         if new_animal not in self.animals:
#             self.animals.append(new_animal)
            
#     def get_animals(self):
#         print(self.animals)
    
#     def sell_animal(self, animal_sold):
#         if animal_sold in self.animals:
#             self.animals.remove(animal_sold)
            
#     def sort_animals(self):
#         sorted_animals = {}
#         for animal in sorted(self.animals):
#             first_letter = animal[0]
#             if first_letter not in sorted_animals:
#                 sorted_animals[first_letter] = []
#             sorted_animals[first_letter].append(animal)
#         return sorted_animals
    
#     def get_groups(self):
#         groups = self.sort_animals()
#         for letter, animals in groups.items():
#             print(f"{letter}: {', '.join(animals)}")
            
            
# abidjan_zoo = Zoo("Abidjan Zoo")
# abidjan_zoo.add_animal("Lion")
# abidjan_zoo.add_animal("Tiger")
# abidjan_zoo.add_animal("Leopard")
# abidjan_zoo.add_animal("Giraffe")
# abidjan_zoo.get_animals()
# abidjan_zoo.sell_animal("Leopard")
# abidjan_zoo.get_animals()
# abidjan_zoo.sort_animals()
# abidjan_zoo.get_groups()



