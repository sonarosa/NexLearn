class Log:
    def __init__(self):  
        self.log = [] 

    def broadcast(self, message):
        """
        Broadcast a message to the player, logging it to combat logs.
        This will be used for combat events or major gameplay moments.
        """
        self.log.append(message)
        print(f'{message}')

    def anchor(self, title, description):
        """
        Log and store a major story event with a title and description.
        Useful for anchoring important story progress.
        """
        event = {
            'title': title,
            'description': description
        }
        self.log.append(event)
        print(f'--- Story Event ---')
        print(f'Title: {title}')
        print(f'Description: {description}')
        print(f'-------------------')

    def clearLogs(self):
        self.combat.clear()

    def showlogs(self):
        print(self.logs)