import random
import game_settings

class Engine():
#    def __init__(self, course, players):
#        self.board = course.board
#        self.spawn = course.spawn
#        self.flags = course.flags
#        self.rules = course.rules

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

if __name__ == "__main__":
    Engine().deal()
