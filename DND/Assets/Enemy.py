class Enemy:
    
    def __init__(self, name, species , role):

        self.name           = name
        self.species        = species
        self.role           = role
        self.level          = 0
        self.vitality       = None
        self.health         = None
        self.attack         = None
        self.agility        = None
        self.resistance     = None
        self.defeated       = False
        self.setStats()

    def generateStats(self):
        pass

    def setStats(self):
        stats           = self.generateStats()
        self.vitality   = stats['vitality']
        self.health     = self.vitality
        self.attack     = stats['attack']
        self.agility    = stats['agility']
        self.resistance = stats['resistance']
        
    def damage(self, amount):
        self.health -= amount
        if self.health <= 0 :
            self.health = 0
            self.defeated = True

    def recover(self, amount):
        self.health += amount
        if self.health > self.vitality :
            self.health = self.vitality 
    
