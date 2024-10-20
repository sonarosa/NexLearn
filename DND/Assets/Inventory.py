from Log import Log
class Inventory:
    def __init__(self):
        self.items = {}
        self.log = Log()

    def addItem(self, item, quantity=1):
        """
        Add an item to the inventory. If the item already exists, increase the quantity.
        """
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def removeItem(self, item, quantity=1):
        """
        Remove a specific quantity of an item from the inventory.
        If the quantity reaches zero, the item is removed entirely.
        """
        if item in self.items:
            if self.items[item] > quantity:
                self.items[item] -= quantity
                self.log.broadcast(f'Used up{quantity} x {item}.')
            elif self.items[item] == quantity:
                del self.items[item]
                print(f'Used {item}')
            else:
                print(f'Not enough items')
        else:
            print(f'{item} is not in the inventory.')

    def showInventory(self):
        """
        Display all items in the inventory along with their quantities.
        """
        if not self.items:
            print('Your inventory is empty.')
        else:
            print('\n--- Inventory ---')
            for item, quantity in self.items.items():
                print(f'{item} (x{quantity})')
            print('-----------------\n')

    def useItem(self, item):
        """
        Use an item from the inventory. The item effect can be healing, buffing, etc.
        After using the item, reduce its quantity in the inventory.
        """
        if item in self.items:
            # Handle item effects here (for example, healing or buffs)
            print(f'You used {item}.')

            # Example of using a healing potion
            if item == 'Healing Potion':
                # Apply healing effect (assuming a `player` object exists)
                healing_amount = 50  # Example value
                print(f'You regained {healing_amount} health.')

            # After using the item, remove it from inventory
            self.remove_item(item, 1)
        else:
            print(f'{item} is not in your inventory.')

    def item(self):
        """
        Returns the first available item from the inventory.
        This is just a placeholder; the player could choose an item via some other mechanism.
        """
        if self.items:
            # Return the first item in the inventory
            return next(iter(self.items))
        else:
            print('No items available in inventory.')
            return None
