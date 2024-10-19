import random
from Enemy import Enemy
from Player import Player
from Dice import Dice
from Log import Log
class Encounter():

    def someFunc():
        pass

    def __init__(self , player , enemy):

        self.title, self.description = self.generateStory()
        self.operations = ['strike' , 'block' , 'use' , 'escape']
        self.playerAction = None
        self.enemy = enemy
        self.player = player
        self.playerHealth = self.player.health
        self.current = 0 if self.player.agility > self.enemy.agility else 1  # 0 -> player , 1 -> enemy
        self.threshold = None
        self.inventory = player.inventory
        self.round = 0
        self.enemyStun = 0
        self.exp = 0
        self.END = False
        self.dice = Dice(20)
        self.log = Log()
    
    def generateStory(self, item = None , status = None):
        # Function to generate a story from the chatbot
        pass

    def strike(self , threshold):
        roll = self.dice.roll()
        crit = 1
        luck = self.dice.roll()
        if roll > threshold :
            if luck > 15 :
                self.log.broadcast('Critical Hit!')
                crit = 2
            damage = ((self.player.attack) * crit) / (self.enemy.resistance // 3)
            self.applyDamageToEnemy(damage = damage)    
        else : 
            self.log.broadcast(f'The target evaded')

    def attack(self , threshold):
        roll = self.dice.roll()
        crit = 1
        luck = self.dice.roll()
        if roll > threshold:
            if luck > 15 :
                self.log.broadcast('Critcal block!, the enemy is stunned for 2 turns')
                crit = 2
                self.enemyStun = 1 * crit
        else :
            if luck < 3 :
                crit = 2
                self.log.broadcast("Enemy dealt critical damage")
            damage = ((self.enemy.attack) * crit ) // (self.player.resistance // 3)
            self.applyDamageToPlayer(damage)

    def enemyAction(self):
        if self.enemyStun == 0:
            self.attack(100)
        else :
            self.log.broadcast('The enemy is stunned')
            self.enemyHealth -= 1

    def escape(self, threshold):
        specialDice = Dice(7)
        roll = specialDice.roll()
        if roll > 5: 
            return True
        else :
            return False
        
    def applyDamageToEnemy(self, damage):
        self.enemy.damage(damage)
        self.Log.broadcast(f'The enemy took {damage} damage.')

    def applyDamageToPlayer(self, damage):
        self.playerHealth -= damage
        self.Log.broadcast(f'You took {damage} damage.')



    def cycle(self): 
        self.round += 1
        threshold = self.dice.roll()
        if self.action == 'strike':
            if self.player.agility > self.enemy.agility :
                self.strike(threshold)
                self.enemyAction()
            else :
                self.enemyAction()
                self.strike(threshold)
        elif self.action == 'block':
            self.enemyAction()
        elif self.action == 'use' :
            self.inventory.showInventory()
            item = self.inventory.item()
            self.log.broadcast(f'You used the item {item}')
            self.effects = self.generateStory(item)
            self.enemyAction()
        else:
            self.END = self.escape()
            if self.END :
                self.log.broadcast('You successfully escaped!')

    def experience(self):
        diff = self.enemy.level - self.player.level
        return diff * 3 

    def checkEnd(self):
        if self.playerHealth < 0 :
            self.log.broadcast('You Lost :( )')
            status = 'lost'
            self.END = True
            self.player.health -= (self.enemy.attack()) // (self.resistance // 3)
            self.effects = self.generateStory(status = status)
        if self.enemy.defeated :
            self.log.broadcast('You Won!')
            self.END = True
            status = 'won'
            self.effects = self.generateStory(status = status)
            self.exp = self.experience()
            self.log.broadcast(f'You gained {self.exp} experience' )

    def getAction(self):
        # function to get action from player
        pass

    def run(self):
        while not self.END:
            action = self.getAction()
            self.cycle(action)
            self.checkEnd()
        self.onEnd()

    def onEnd(self):
        self.log.broadcast('Game has ended')
        self.log.clearCombatLogs()
        return self.exp , self.effects



