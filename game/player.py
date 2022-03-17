class Player:
    """
    docstring for Player.
    """

    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.chips_in_front = 0

    def move_chips(self, amount):
        self.chips += amount

    def bet(self, amount):
        self.chips_in_front += amount
        self.chips -= amount
