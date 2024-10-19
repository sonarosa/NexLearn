class Quest:
    def __init__(self):
        self.title = None
        self.description = None
        self.completed = False
        self.options = []
        self.chosenOption = None

    def getQuest(self):
        pass

    def chooseOption(self):
        pass

    def generateResult(self):
        pass

    def generateQuests(self):
        self.title , self,description  = self.someFunc()
        self.options = self.someFunc()
        self.completed = False

    def chooseOption(self, option):
        self.chosenOption = option
        self.generateResult()
        self.completed = True