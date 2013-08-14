import random
from game_settings import *

class Engine():
    def __init__(self, course, players):
        self.filename = course.filename
        self.board = course.board
        self.spawn = course.spawn
        self.flags = course.flags
        self.rules = course.rules
        self.players = []

        for i, player in enumerate(players):
            health = []
            for j in range(START_HEALTH):
                health.append(1)
            for j in range(MAX_HEALTH - START_HEALTH):
                health.append(0)

            self.players.append(Player(
                player,
                index=i,
                lives=MAX_LIVES,
                health=health,
                archive=course.spawn[i],
                orientation=0, #orientation,
            ))
            self.players[-1].spawn()

    def deal(self):
        deck = [Card(p) for p in range(10, 850, 10)]
        random.shuffle(deck)
        print deck

    def main(self, user_cards):
        #user_cards should be a dict containing player index, then card {1:self.deck[10], etc.}
        assert type(user_cards) == dict
        play_order = sorted(user_cards, key=lambda x: x[1])

        for player, card in play_order:
            if card.card == "Move 1":
                pass
            elif card.card == "Move 2":
                pass
            elif card.card == "Move 3":
                pass
            elif card.card == "Back Up":
                pass
            elif card.card == "Rotate Left":
                pass
            else:
                pass

#            if player.isOn = LASER1 etc.

class Card():
    def __init__(self, priority):
        assert 10 <= priority <= 840
        assert priority % 10 == 0
        self.priority = priority
        cards = {
            10: "U-Turn",
            70: "Rotate Left",
            440: "Back Up",
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
        self.coords = self.archive

if __name__ == "__main__":
#    game = Engine(None, ["Sam", "Matt"])
    pass
