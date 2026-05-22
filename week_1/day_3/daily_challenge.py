class Farm:
    def __init__(self, farm_name):
        self.farm_name = farm_name
        self.animals = {}

    def add_animal(self, animal_type, count=1):
        # Backwards-compatible: allow single animal add via (animal_type, count)
        # Also support adding multiple animals using keyword arguments: add_animal(cow=5, sheep=2)
        if animal_type is not None:
            if animal_type in self.animals:
                self.animals[animal_type] += count
            else:
                self.animals[animal_type] = count

    def add_animals(self, **kwargs):
        # Helper to add multiple animals at once using kwargs
        for animal_type, qty in kwargs.items():
            if animal_type in self.animals:
                self.animals[animal_type] += qty
            else:
                self.animals[animal_type] = qty
            
    def get_info(self):
        print(f"{self.farm_name} has:")
        for animal, count in self.animals.items():
            print(f"{animal} : {count}")
        print("\nE-I-E-I-Oh!")
        
    def get_animal_types(self):
        return sorted(self.animals.keys())
    
    def get_short_info(self):
        animal_types = self.get_animal_types()
        if not animal_types:
            print(f"{self.farm_name} has no animals.")
            return

        display_names = []
        for animal in animal_types:
            count = self.animals.get(animal, 0)
            name = animal if count == 1 else animal + 's'
            display_names.append(name)

        if len(animal_types) == 1:
            animal = animal_types[0]
            count = self.animals.get(animal, 0)
            name = animal if count == 1 else animal + 's'
            print(f"{self.farm_name} has {count} {name}.")
        else:
            print(f"{self.farm_name} has {len(self.animals)} types of animals: {', '.join(display_names)}.")
            
    
      
my_farm = Farm("Old MacDonald's Farm")
my_farm.add_animal("cow", 5)
my_farm.add_animal("chicken", 10)
my_farm.add_animal("pig", 3)
my_farm.add_animal("sheep", 1)
my_farm.get_info()
my_farm.get_short_info()
        
    