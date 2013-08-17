import random
from game_settings import *

class Engine():
    def __init__(self, course, players, lobby):
        self.actions = {}
        self.lobby = lobby
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

        self.deal()

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
            if not 0 <= x1 < len(self.board[0]) and 0 <= y1 <= len(self.board):
                return False
            if countbots and self.get_player(x1, y1) is not None:
                return self.get_player(x1, y1)
            if self.board[y1][x1].walls[opp] != BLANK:
                return True
        return False

    def move(self):
        for player in self.players:
            player.confirmed = False
            if not player.alive:
                player.spawn()
        self.deal()
        self.flush_notifications()

    def run_move(self):
        if not all([p.confirmed for p in self.players]):
            return

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
            self.flush_notifications()

        for player in self.players:
            player.try_heal()

        self.move()

    def get_player(self, x, y):
        for player in self.players:
            if player.pos() == (x, y) and not player.virtual:
                return player

    def conveyer(self, normal=False):
        conveyers = [CONVEYER2] + [CONVEYER1]*normal
        for player in self.players:
            if player.alive and player.square().square in conveyers:
                exit = player.square().exit
                player.move(exit)
                if player.square().square in [CONVEYER1, CONVEYER2]:
                    entrance = exit
                    exit = player.square().exit
                    if (8 - entrance) % 4 in player.square().entrances:
                        player.rot(exit - entrance + 4)

    def push_pushers(self, register):
        active = PUSHER24 if register % 2 else PUSHER135
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
        self.actions[action] = self.actions.get(action, []) + [text]
        if flush:
            self.flush_notifications()

    def flush_notifications(self):
        for action in self.actions:
            self.lobby.message(
                None,
                action,
                '\n'.join(self.actions[action]),
            )

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
        self.robot = [
            "hammer_bot",
            "hulk_x90",
            "spin_bot",
            "squash_bot",
            "trundle_bot",
            "twitch",
            "twonky",
            "zoom_bot",
        ][self.index]

    def deal(self, cards):
        self.cards = cards
        self.game.lobby.message(self.user, 'dealhand', ' '.join(
            ['%s,%d' % (card.file, card.priority) for card in self.cards]
        ))

    def spawn(self):
        self.alive = True
        self.orientation = 1
        for player in self.game.players:
            if player != self and player.pos() == self.archive:
                self.virtual = True
        self.x, self.y = self.archive
        self.notify_move()

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

    def notify_move(self):
        self.game.add_notification(
            'move',
            '%d %d %d %d %d' % (self.index, 2, self.x, self.y, self.orientation)
        )

    def ready(self):
        self.confirmed = True
        self.game.run_move()

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
        self.notify_move()
    
    def in_bounds(self):
        board = self.game.board
        return 0 <= self.x < len(board[0]) \
            and 0 <= self.y < len(board) \
            and board[self.y][self.x].square != PIT

    def kill(self):
        self.alive = False
        self.x = self.y = -1
        self.health = [1] * (MAX_HEALTH - 2) + [0, 0]
        self.notify_move()

    def rot(self, amount):
        self.orientation += 4 + amount
        self.orientation %= 4
        self.notify_move()

    def try_heal(self, amount=1):
        if self.pos() in self.game.flags or \
                self.game.board[self.y][self.x].square in [REPAIR, HAMMER_AND_WRENCH]:
            for i in range(amount):
                if 0 in self.health:
                    self.health[self.health.index(0)] = 1
        self.game.add_notification('health',
                '%d %s' % (self.index, ','.join(map(str, self.health))))


    def reach(self):
        if self.pos() == self.game.flags[self.flag]:
            self.flag += 1
        if self.pos() != self.archive and (self.pos() in self.game.flags or \
                self.game.board[self.y][self.x].square in [REPAIR, HAMMER_AND_WRENCH]):
            self.archive = self.pos()
            self.game.add_notification(
                'move',
                '%d %d %d %d %d' % (self.index, 1, self.x, self.y, 0)
            )

    def square(self):
        if self.alive:
            return self.game.board[self.y][self.x]

    def swapcards(self, c1, c2):
        self.cards[c1], self.cards[c2] = self.cards[c2], self.cards[c1]

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

        self.file = {
                        UTURN: 'uturn',
                        ROTLEFT: 'rotleft',
                        ROTRIGHT: 'rotright',
                        BACKUP: 'backup',
                        MOVE1: 'move1',
                        MOVE2: 'move2',
                        MOVE3: 'move3',
                        }[self.card]

    def __repr__(self):
        return '%s (%d)' % (self.card, self.priority)

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.card == other

if __name__ == "__main__":
    pass
