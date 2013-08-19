import random
from game_settings import *

class Engine():
    def __init__(self, course, players, lobby):
        self.actions = {}
        self.lobby = lobby
        self.filename = course.filename
        self.board = course.board
        self.spawn = course.spawn
        self.flags = [tuple(flag) for flag in course.flags]
        self.rules = course.rules
        self.players = []

        self.options = set(OPTION_DESC)

        for i, player in enumerate(players):
            self.players.append(Player(
                user=player,
                index=i,
                lives=MAX_LIVES, # should we play with bonuses
                health=MAX_HEALTH,
                archive=tuple(course.spawn[i]),
                orientation=1, # relative to up, 1 per dir
                game=self,
            ))
            self.players[-1].spawn(notify=False)

        self.deal()

    def blocked(self, (x1, y1), (x2, y2), countbots=False, side=None):
        assert (x1 == x2) != (y1 == y2) or (x2, y2) == (None, None)
        if side == None:
            if x1 > x2:
                side = 3
            elif x1 < x2:
                side = 1
            elif y1 > y2:
                side = 0
            elif y1 < y2:
                side = 2
        opp = (6 - side) % 4
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][side]

        while (x1, y1) != (x2, y2) or (x2, y2) == (None, None):
            if self.board[y1][x1].walls[side] != BLANK:
                return True
            x1 += dx
            y1 += dy
            if not (0 <= x1 < len(self.board[0]) and 0 <= y1 < len(self.board)):
                return False
            if countbots and self.get_player(x1, y1) is not None:
                return self.get_player(x1, y1)
            if self.board[y1][x1].walls[opp] != BLANK:
                return True
        return False

    def move(self):
        virtual = set()
        for player in self.players:
            player.confirmed = False
            if not player.alive:
                player.spawn()
            for player in self.players:
                player.virtual = False
                for bot in self.players:
                    if bot.pos() == player.pos() and bot != player:
                        player.virtual = True
                        virtual.add(player.index)

        if not any([player.alive for player in self.players]):
            self.add_notification('restart', '', flush=True)
            del self.lobby.games[self.lobby.name]
            return # just in case it infinite loops...

        self.add_notification('virtual', ' '.join(map(str, virtual)))
        self.deal()
        self.run_move()
        self.flush_notifications()

    def run_move(self):
        if not all([p.confirmed for p in self.players]):
            return

        for register in range(5):
            for player in sorted(self.players, key=lambda x: x.cards[register]):
                if player.power_down != 0 and player.alive:
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
            if player.power_down != 0:
                player.try_heal()
            player.power_down -= 1
            if CIRCUIT_BREAKER in player.options and player.health <= MAX_HEALTH - 3:
                player.power_down = 0
            if player.power_down == 0:
                # heal
                player.locked = []
                player.health = MAX_HEALTH
            self.lobby.message(player.user, 'health', '%d %d' % (player.lives, player.health))

        self.move()

    def get_player(self, x, y):
        for player in self.players:
            if player.pos() == (x, y) and not player.virtual:
                return player

    def conveyer(self, normal=False):
        res = []
        conveyers = [CONVEYER2] + [CONVEYER1]*normal
        for player in self.players:
            if player.alive and player.square().square in conveyers:
                exit = player.square().exit
                pushed = player.move(exit, conveyers=conveyers)
                if player.square() is not None and player.square().square in [CONVEYER1, CONVEYER2]:
                    entrance = (exit + 2) % 4
                    exit = player.square().exit
                    if entrance in player.square().entrances:
                        player.rot(2 - entrance + exit)
                for player in pushed:
                    res.append(player.notify_move(False))
        self.add_notification(
            'move',
            ' '.join(res)
        )

    def push_pushers(self, register):
        res = []
        active = PUSHER24 if register % 2 else PUSHER135
        for player in self.players:
            if player.square() is not None:
                for side, wall in enumerate(player.square().walls):
                    if wall == active:
                        pushed = player.move((6 - side) % 4)
                        for player in pushed:
                            res.append(player.notify_move(False))
        self.add_notification(
            'move',
            ' '.join(res)
        )

    def rotate_gears(self):
        res = []
        for player in self.players:
            if self.board[player.y][player.x].square == RED_GEAR:
                player.rot(-1)
                res.append(player.notify_move(False))
            elif self.board[player.y][player.x].square == GREEN_GEAR:
                player.rot(1)
                res.append(player.notify_move(False))
        self.add_notification('move', ' '.join(res))

    def fire_lasers(self):
        for y, row in enumerate(self.board):
            for x, square in enumerate(row):
                for i, side in enumerate(square.walls):
                    if side in LASERS:
                        bot = self.get_player(x, y)
                        if bot is None:
                            bot = self.blocked((x, y), (None, None), countbots=True, side=(6-i)%4)
                        if isinstance(bot, Player):
                            bot.damage(LASERS.index(side) + 1)

        for player in self.players:
            if player.power_down != 0 and not player.virtual:
                bot = self.blocked((player.x, player.y), (None, None), countbots=True, side=player.orientation)
                if isinstance(bot, Player) and not bot.virtual:
                    bot.damage(1 + int(DOUBLE_BARRELED_LASER in player.options))

            if REAR_FIRING_LASER in player.options:
                bot = self.blocked((player.x, player.y), (None, None), countbots=True, side=(2+player.orientation) % 4)
                if isinstance(bot, Player) and not bot.virtual:
                    bot.damage()



    def deal(self):
        self.deck = [Card(p) for p in range(10, 850, 10)]
        for player in self.players:
            if FLYWHEEL in player.options:
                player.flywheel = None
                if player.cards is not None and len(player.cards) > 5:
                    player.flywheel = player.cards[-1]

        for player in self.players:
            for card in self.deck:
                if card in player.locked:
                    card.locked = True
        self.deck = list(filter(lambda x: not x.locked, self.deck))
        random.shuffle(self.deck)
        for player in self.players:
            if player.power_down != 0:
                player.deal(self.deck[-player.num_cards():])
            else:
                player.confirmed = True
                self.lobby.message(player.user, 'dealhand', '')
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
                '\n'.join(filter(bool, self.actions[action])),
            )
        self.actions = {}

class Player():
    def __init__(self, **kwargs):
        self.confirmed = False
        self.virtual = False
        self.flag = 0
        self.cards = None
        self.x = self.y = None
        self.locked = [] # locked in reverse order - registers go 5 to 1
        self.options = set()
        self.last_pos = ''
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

        # add options for testing here
        # self.get_option(POWER_DOWN_SHIELD)

    def deal(self, cards):
        self.cards = cards + self.locked[::-1]

        if EXTRA_MEMORY in self.options:
            self.cards.append(self.game.deck[-1])
            self.game.deck.pop()

        if FLYWHEEL in self.options and self.flywheel is not None:
            self.cards.append(self.flywheel)

        self.game.lobby.message(self.user, 'dealhand', ' '.join(
            ['%s,%d,%d' % (card.file, card.priority, int(card.locked)) for card in self.cards]
        ))

    def spawn(self, notify=True):
        if self.lives > 0:
            self.alive = True
            self.power_down = -1
            self.orientation = 1
            self.x, self.y = self.archive
            if notify:
                self.notify_move()
        else:
            self.power_down = 0 # ensure they don't get dealt cards
            self.confirmed = True

    def run_register(self, register):
        if self.alive:
            card = self.cards[register]
            pushed = [self]
            if card == MOVE1:
                pushed = self.move()
            elif card == MOVE2:
                pushed = self.move(dis=2)
            elif card == MOVE3:
                pushed = self.move(dis=3)
            elif card == BACKUP:
                self.rot(2)
                pushed = self.move()
                self.rot(2)
            elif card == ROTLEFT:
                self.rot(-1)
            elif card == ROTRIGHT:
                self.rot(1)
            elif card == UTURN:
                self.rot(2)
            else:
                raise ValueError("Player card was %s. Should have been a proper move" % card.card)

            res = []
            for player in pushed:
                res.append(player.notify_move(False))
            self.game.add_notification(
                'move',
                ' '.join(res)
            )

    def notify_move(self, notify=True):
        opacity = 0.5 if self.virtual else 1
        move = '%d %d %d %d %d' % (self.index, 2, self.x, self.y, self.orientation)
        if notify and move != self.last_pos:
            self.game.add_notification('move', move)
            last_pos = move
        return move

    def ready(self):
        self.confirmed = True
        self.game.run_move()

    def program_cards(self):
        return [] if self.cards is None else self.cards[:5]

    def hand(self):
        return [] if self.cards is None or self.power_down == 0 else self.cards[5:]

    def num_cards(self):
        return self.health

    def pos(self):
        return (self.x, self.y)

    def move(self, direction=None, dis=1, conveyers=[]):
        orig = self.pos()
        pushed = [self]
        hit = None
        for i in range(dis):
            if direction is None:
                direction = self.orientation
            dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][direction]
            nx = self.x + dx
            ny = self.y + dy
            bot = self.game.get_player(nx, ny)
            blocked = False
            if not self.virtual and bot is not None and not bot.virtual and \
                    bot.square().square not in conveyers:
                hit = bot
                moved = bot.move(direction)
                pushed += moved
                if not moved: blocked = True
            if not self.game.blocked(self.pos(), (nx, ny)) and not blocked:
                self.x = nx
                self.y = ny
            if not self.in_bounds():
                self.kill()
        if hit is not None:
            if RAMMING_GEAR in hit.options:
                self.damage()
            if RAMMING_GEAR in self.options:
                hit.damage()
        if orig == self.pos(): # no-one moved
            return []
        else:
            return pushed

    def in_bounds(self):
        board = self.game.board
        return 0 <= self.x < len(board[0]) \
            and 0 <= self.y < len(board) \
            and board[self.y][self.x].square != PIT

    def kill(self):
        self.alive = False
        self.x = self.y = -1
        self.health = MAX_HEALTH
        if SUPERIOR_ARCHIVE not in self.options:
            self.damage(2)
        self.lives -= 1
        self.locked = []
        self.notify_move()

    def rot(self, amount):
        self.orientation += 4 + amount
        self.orientation %= 4

    def damage(self, amount=1):
        assert amount > 0
        if self.power_down == 0 and POWER_DOWN_SHIELD in self.options:
            amount -= 1

        for i in range(amount):
            if ABLATIVE_COAT in self.options:
                self.ablative_coat_health -= 1
                if self.ablative_coat_health <= 0:
                    self.delete_option(ABLATIVE_COAT)
            else:
                self.health -= 1

            if self.health < 0:
                self.kill()
                break # don't hurt them any more. They're already dead
            elif self.health < 5:
                self.locked.append(self.cards[self.health])
                self.locked[-1].locked = True

    def try_heal(self):
        if not self.alive: return
        if self.pos() in self.game.flags or \
                self.square().square in [REPAIR, HAMMER_AND_WRENCH]:
            if self.health != MAX_HEALTH:
                if self.health < 5:
                    self.locked.pop()
                self.health += 1
        if self.square().square == HAMMER_AND_WRENCH:
            self.get_option()

    def option_list(self):
        return [OPTION_DESC[option] for option in self.options]

    def get_option(self, force=None):
        assert force is None or force in OPTION_DESC
        option = force
        if force is None and self.game.options:
            option = random.choice(list(self.game.options))
        if option is not None and option in self.game.options:
            self.game.options.remove(option)
            self.options.add(option)
            if not force:
                self.game.lobby.message(self.user, 'options', '+' + OPTION_DESC[option])
            if option == ABLATIVE_COAT:
                self.ablative_coat_health = 3

    def delete_option(self, option):
        assert option in self.options
        self.options.remove(option)
        self.game.options.add(option)
        self.game.lobby.message(self.user, 'options', '-' + OPTION_DESC[option])

    def reach(self):
        if not self.alive: return
        if self.pos() == self.game.flags[self.flag]:
            self.flag += 1
            if self.flag == len(self.game.flags):
                self.game.add_notification(
                    "alert",
                    "%s has finished. However, you can still keep on playing." % self.user.username
                )
        if self.pos() != self.archive and (self.pos() in self.game.flags or \
                self.square().square in [REPAIR, HAMMER_AND_WRENCH]):
            self.archive = self.pos()
            self.game.add_notification(
                'move',
                '%d %d %d %d 0' % (self.index, 1, self.x, self.y)
            )
            self.game.lobby.message(self.user, 'newobjective', str(self.flag+1))

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
        self.locked = False
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
        if isinstance(other, str):
            return self.card == other
        elif isinstance(other, Card):
            return self.priority == other.priority
