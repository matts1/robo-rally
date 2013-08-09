import random
from game_settings import *

class Engine():
    def __init__(self, course, players):
        self.board = course.board
        self.spawn = course.spawn
        self.flags = course.flags
        self.rules = course.rules
        self.players = []

        for i, player in enumerate(players):
            health = []
            for i in range(START_HEALTH):
                health.append(1)
            for i in range(MAX_HEALTH - START_HEALTH):
                health.append(0)

            self.players.append(Player(
                player,
                lives=MAX_LIVES,
                health=health,
                spawn=course.spawn[i],
            ))
            self.players[-1].spawn()


    def deal(self):
        deck = [Card(p) for p in range(10, 850, 10)]
        random.shuffle(deck)
        print deck

class Card():
    def __init__(self, priority):
        assert 10 <= priority <= 840
        assert priority % 10 == 0
        self.priority = priority
        cards = {
            10: "U-Turn",
            70: "Rotate Left",
            440: "Back up",
            540: "Move 1",
            660: "Move 2",
            790: "Move 3"
        }
        for card in sorted(cards):
            if priority >= card:
                self.card = cards[card]
        if self.card == "Rotate Left" and priority % 20 == 0:
            self.card = "Rotate Right"

    def __repr__(self):
        return "%s (%d)" % (self.card, self.priority)

class Player():
    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

    def spawn(self):
        self.coords = self.spawn

if __name__ == "__main__":
#    game = Engine(None, ["Sam", "Matt"])
    pass