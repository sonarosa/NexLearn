class Player:
    
    def __init__(self, name, species , job):
        
        self.SPECIES = {
            'elf' : {
                'vitality'  : 80,
                'attack'    : 15,
                'agility'   : 30,
                'stealth'   : 15,
                'charisma'  : 30,
                'resistance': 10,
                'wisdom'    : 20,
                'mana'      : 30
            },
            'dwarf' : {
                'vitality'  : 120,
                'attack'    : 25,
                'agility'   : 15,
                'stealth'   : 10,
                'charisma'  : 15,
                'resistance': 30,
                'wisdom'    : 30,
                'mana'      : 30
            },
            'human' : {
                'vitality'  : 100,
                'attack'    : 20,
                'agility'   : 20,
                'stealth'   : 15,
                'charisma'  : 30,
                'resistance': 10,
                'wisdom'    : 20,
                'mana'      : 10
            },
            'orc' : {
                'vitality'  : 150,
                'attack'    : 30,
                'agility'   : 10,
                'stealth'   : 5,
                'charisma'  : 5,
                'resistance': 40,
                'wisdom'    : 5,
                'mana'      : 5
            }
        }
        self.JOBS = {
            'warrior' : {
                'vitality'  : 20,
                'attack'    : 30,
                'agility'   : 0,
                'stealth'   : 0,
                'charisma'  : 5,
                'resistance': 30,
                'wisdom'    : 0,
                'mana'      : 0
            },
            'mage' : {
                'vitality'  : 0,
                'attack'    : 30,
                'agility'   : 10,
                'stealth'   : 0,
                'charisma'  : 10,
                'resistance': 0,
                'wisdom'    : 5,
                'mana'      : 30
            },
            'thief' : {
                'vitality'  : 0,
                'attack'    : 15,
                'agility'   : 30,
                'stealth'   : 30,
                'charisma'  : -5,
                'resistance': 0,
                'wisdom'    : 10,
                'mana'      : 0
            },
            'rogue' : {
                'vitality'  : 0,
                'attack'    : 40,
                'agility'   : 20,
                'stealth'   : 0,
                'charisma'  : 5,
                'resistance': 0,
                'wisdom'    : 20,
                'mana'      : 0
            }
        }

        self.name           = name
        self.species        = species
        self.job            = job
        self.level          = 0
        self.experience     = 0
        self.points         = 0
        self.quests         = []
        self.activeQuests   = []
        self.GAMELOST       = False
        self.vitality       = None
        self.health         = None
        self.attack         = None
        self.agility        = None
        self.stealth        = None
        self.charisma       = None
        self.resistance     = None
        self.wisdom         = None
        self.mana           = None
        self.setStats()

    def setStats(self):
        speciesStats    = self.SPECIES[self.species]
        jobsStats       = self.JOBS[self.job]
        self.vitality   = speciesStats['vitality'] + jobsStats['vitality'] 
        self.health     = self.vitality
        self.attack     = speciesStats['attack'] + jobsStats['attack']
        self.agility    = speciesStats['agility'] + jobsStats['agility']
        self.stealth    = speciesStats['stealth'] + jobsStats['stealth']
        self.charisma   = speciesStats['charisma'] + jobsStats['charisma']
        self.resistance = speciesStats['resistance'] + jobsStats['resistance']
        self.wisdom     = speciesStats['wisdom'] + jobsStats['wisdom']
        self.mana       = speciesStats['mana'] + jobsStats['mana']

    def upgradeStats(self, stat , point):
        amount = point * 3
        if stat == 'vitality':
            self.vitality   += amount
        if stat == 'attack' :
            self.attack     += amount
        if stat == 'agility' :
            self.agility    += amount
        if stat == 'stealth' :
            self.stealth    += amount
        if stat == 'charisma':
            self.charisma   += amount
        if stat == 'resistance' :
            self.resistance += amount
        if stat == 'wisdom':
            self.wisdom     += amount
        if stat == 'mana':
            self.mana       += amount

    def levelUP(self):
        while self.experience > 100 :
            self.experience = self.experience - 100
            self.level += 1
            self.points += 5

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0 :
            self.GAMELOST = True

    def recover(self, amount):
        self.health += amount
        if self.health > self.vitality :
            self.health = self.vitality 
    
    def revive(self):
        self.vitality -= 20
        self.health = self.vitality
        self.GAMELOST = False

    def completeQuest(self, quest):
        if quest in self.activeQuests: 
            quest.completeQuest()
            self.pastQuests.append(quest)
            self.activeQuests.remove(quest)
            self.experience += quest.experience()
            if self.experience > 100 :
                self.levelUP()

