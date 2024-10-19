import random
class Dice():
    
    def __init__(self, sides = 20):
        
        self.sides = sides

    def roll(self , times):
        return [random.randint(1, self.sides) for _ in range(times)]