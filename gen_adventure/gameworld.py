import random


environments = ["forest", "clearing", "field", "village", "house", "beach"]
creatures = ["goblin", "woman", "man", "dog", "child", "horse"]
things = ["sword", "tankard", "coin", "sack"]


class Place:
    environment : str
    creatures : list
    things : list
    exits : list #Place
    description: str

    def __init__(self, environment, parent_place):
        self.description = ""
        self.environment = environment
        self.creatures = [random.choice(creatures) for a in range(random.randint(0,4))]
        self.things = [random.choice(things) for a in range(random.randint(0,4))]
        if parent_place is not None:
            self.exits = [parent_place]
        else:
            self.exits = []

    def build_exits(self):
        # Generate exist
        exit_environments = list(set([random.choice(environments) for a in range(random.randint(0,4))]))
        # Remove duplicates
        for existing in self.get_exit_environments():
            try:
                exit_environments.remove(existing)
            except ValueError:
                pass
        for exit_environment in exit_environments:
            self.exits.append(Place(exit_environment, self))
    
    def get_exit_environments(self):
        return [exit.environment for exit in self.exits]
    
    def __str__(self):
        return f"Place({self.environment}, {self.get_exit_environments()}, {self.creatures}, {self.things})"   

class World:
    weather : str
    time: str
    root: Place

    def __init__(self):
        self.weather = 'sunny'
        self.time = 'noon'
        self.root = Place("village", None)
        self.root.build_exits()
    
    def __str__(self):       
        return f"World({self.weather}, {self.time}, {self.root})"

