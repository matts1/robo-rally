from copy import deepcopy
import random
from game_settings import *

class Engine():
    def __init__(self, course, players, lobby):
        self.filename = course.filename
        self.board = course.board
        self.spawn = course.spawn
        self.flags = course.flags
        self.rules = course.rules
        self.players = []

        for i, player in enumerate(players):
            self.players.append(Player(
                user=player,
                index=i,
                lives=MAX_LIVES, # should we play with bonuses
                health=[1] * MAX_HEALTH,
                archive=course.spawn[i],
                orientation=1, # relative to up, 1 per dir
                game=self,
            ))
            self.players[-1].spawn()

        self.text = []
        self.actions = []

    def game_over(self):
        for player in self.players:
            if player.flag == len(self.flags):
                return player

    def blocked(self, (x1, y1), (x2, y2), countbots=False):
        assert (x1 == x2) != (y1 == y2)
        if x1 > x2:
            side = 3
        elif x1 < x2:
            side = 1
        elif y1 > y2:
            side = 0
        elif y1 < y2:
            side = 2
        opp = (8 - side) % 4
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][side]

        while (x1, y1) != (x2, y2):
            if self.board[y1][x1].walls[side] != BLANK:
                return True
            x1 += dx
            y1 += dy
            if countbots and self.get_player(x1, y1) is not None:
                return self.get_player(x1, y1)
            if self.board[y1][x1].walls[opp] != BLANK:
                return True
        return False

    def move(self):
        for player in self.players:
            if not player.alive:
                player.spawn()
        self.deal()

        while not all([p.confirmed for p in self.players]):
            pass
        # TODO: LET USERS ARRANGE PROGRAM CARDS HERE AND DO OTHER INPUT

        for register in range(5):
            for player in sorted(self.players, key=lambda x: x.cards[register]):
                player.run_register(register)
            self.conveyer()
            self.conveyer(normal=True)
            self.push_pushers(register)
            self.rotate_gears()
            self.fire_lasers()
            for player in self.players:
                player.reach()

        for player in self.players:
            player.try_heal()

    def get_player(self, x, y):
        for player in self.players:
            if player.pos() == (x, y) and not player.virtual:
                return player

    def conveyer(self, normal=False):
        pass # move the conveyers 1 space.
        # If normal is true, normal conveyers move as well as express

    def push_pushers(self, register):
        active = PUSHER135 if register % 2 else PUSHER24
        for player in self.players:
            for side, wall in enumerate(self.board[player.y][player.x].walls):
                if wall == active:
                    player.move((8 - side) % 4)

    def rotate_gears(self):
        for player in self.players:
            if self.board[player.y][player.x].square == RED_GEAR:
                player.rot(-1)
            elif self.board[player.y][player.x].square == GREEN_GEAR:
                player.rot(1)

    def fire_lasers(self):
        # FIRE BOARD LASERS
        for player in self.players:
            pass # FIRE PLAYER's LASERS

    def deal(self):
        self.deck = [Card(p) for p in range(10, 850, 10)]
        random.shuffle(self.deck)
        for player in self.players:
            player.deal(self.deck[-player.num_cards():])
            self.deck = self.deck[:-player.num_cards()]

    def add_notification(self, action, text, flush=False):
        self.actions.append(action)
        self.text.append(text)
        if flush:
            self.flush_notifications()

    def flush_notifications(self):
        self.lobby.message(None, '\n'.join(self.actions), '\n'.join(self.text))

class Card():
    def __init__(self, priority):
        assert 10 <= priority <= 840
        assert priority % 10 == 0
        self.priority = priority
        cards = {
            10: UTURN,
            70: ROTLEFT,
            430: BACKUP,
            540: MOVE1,
            670: MOVE2,
            790: MOVE3
        }
        for card in sorted(cards):
            if priority >= card:
                self.card = cards[card]
        if self.card == ROTLEFT and priority % 20 == 0:
            self.card = ROTRIGHT

    def __repr__(self):
        return "%s (%d)" % (self.card, self.priority)

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.card == other

class Player():
    def __init__(self, **kwargs):
        self.confirmed = False
        self.virtual = False
        self.flag = 0
        self.cards = None
        self.x = self.y = None
        # set everything from kwargs as attributes
        for k, v in kwargs.items():
            setattr(self, k, v)

    def deal(self, cards):
        self.cards = cards
        # TODO: send notification

    def spawn(self):
        self.alive = True
        for player in self.game.players:
            if player != self and player.pos() == self.archive:
                self.virtual = True
        self.x, self.y = self.archive

    def run_register(self, register):
        card = self.cards[register]
        if card == MOVE1:
            self.move()
        elif card == MOVE2:
            self.move()
            self.move()
        elif card == MOVE3:
            self.move()
            self.move()
            self.move()
        elif card == BACKUP:
            self.rot(2)
            self.move()
            self.rot(2)
        elif card == ROTLEFT:
            self.rot(-1)
        elif card == ROTRIGHT:
            self.rot(1)
        elif card == UTURN:
            self.rot(2)
        else:
            raise ValueError("Player card was %s. Should have been a proper move" % card.card)

    def program_cards(self):
        return [] if self.cards is None else self.cards[:5]

    def hand(self):
        return [] if self.cards is None else self.cards[5:]

    def num_cards(self):
        return 9 - self.health.count(0)

    def pos(self):
        return (self.x, self.y)

    def move(self, direction=None):
        if direction is None:
            direction = self.orientation
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][direction]
        nx = self.x + dx
        ny = self.y + dy
        if self.game.get_player(nx, ny) is not None:
            self.game.get_player(nx, ny).move(direction)
        if not self.game.blocked(self.pos(), (nx, ny)):
            self.x = nx
            self.y = ny
        if not self.in_bounds():
            self.kill()
    
    def in_bounds(self):
        board = self.game.board
        return 0 <= self.x < len(board[0]) \
            and 0 <= self.y < len(board) \
            and board[self.y][self.x].square != PIT

    def kill(self):
        self.alive = False
        self.x = self.y = None
        self.health = [1] * (MAX_HEALTH - 2) + [0, 0]

    def rot(self, amount):
        self.orientation += 4 + amount
        self.orientation %= 4

    def try_heal(self, amount=1):
        if self.pos() in self.game.flags or \
                self.game.board[self.y][self.x].square in [REPAIR, HAMMER_AND_WRENCH]:
            for i in range(amount):
                if 0 in self.health:
                    self.health[self.health.index(0)] = 1

    def reach(self):
        if self.pos() == self.game.flags[self.flag]:
            self.flag += 1
        if self.pos() in self.game.flags or \
                self.game.board[self.y][self.x].square in [REPAIR, HAMMER_AND_WRENCH]:
            self.archive = self.pos()

if __name__ == "__main__":
    pass
