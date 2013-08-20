# MUST MATCH THE INDEXES IN THE LIST 'INDEXES_TO_FILES'
BLANK = 8
WALL = 25
LASER1 = 22
LASER2 = 6
LASER3 = 23
PUSHER135 = 24
PUSHER24 = 7
PIT = 13
FLOOR = 9
CONVEYER1 = 19
CONVEYER2 = 3
GREEN_GEAR = 10
RED_GEAR = 14
REPAIR = 15
HAMMER_AND_WRENCH = 11

LASERS = [LASER1, LASER2, LASER3]

SQUARE_SIDES = {
    'b': BLANK,
    'w': WALL,
    'l': LASER1,
    'd': LASER2,
    't': LASER3,
    'p': PUSHER135,
    'v': PUSHER24
}

SQUARE_CONTENTS = {
    'p': PIT,
    'f': FLOOR,
    'g': GREEN_GEAR,
    'o': RED_GEAR,
    'c': CONVEYER1,
    'x': CONVEYER2,
    'r': REPAIR,
    'h': HAMMER_AND_WRENCH
}

DIRECTIONS = {
    'n': 0,
    'e': 1,
    's': 2,
    'w': 3
}

FILES = {
    FLOOR: 'floor',
    PIT: 'pit',
    CONVEYER1: 'singleconveyer',
    CONVEYER2: 'doubleconveyer',
    GREEN_GEAR: 'greengear',
    RED_GEAR: 'redgear',
    REPAIR: 'repair',
    HAMMER_AND_WRENCH: 'hammerwrench',
    BLANK: 'empty',
    WALL: 'wall',
    LASER1: 'singlelaser',
    LASER2: 'doublelaser',
    LASER3: 'triplelaser',
    PUSHER135: 'triplepusher',
    PUSHER24: 'doublepusher',
}

INDEXES_TO_FILES = '''doubleconveyerconvergeanticlockwise.png
doubleconveyerconvergeclockwise.png
doubleconveyerconverge.png
doubleconveyerstraight.png
doubleconveyerturnanticlockwise.png
doubleconveyerturnclockwise.png
doublelaser.png
doublepusher.png
empty.png
floor.png
greengear.png
hammerwrench.png
laser.png
pit.png
redgear.png
repair.png
singleconveyerconvergeanticlockwise.png
singleconveyerconvergeclockwise.png
singleconveyerconverge.png
singleconveyerstraight.png
singleconveyerturnanticlockwise.png
singleconveyerturnclockwise.png
singlelaser.png
triplelaser.png
triplepusher.png
wall.png'''.split('\n')

FILES_TO_INDEXES = dict([x[::-1] for x in enumerate(INDEXES_TO_FILES)])

TIMEOUT = 20

# GAME SETTINGS
BACKUP = 'Back Up'
MOVE1 = 'Move 1'
MOVE2 = 'Move 2'
MOVE3 = 'Move 3'
UTURN = 'U-Turn'
ROTLEFT = 'Rotate Left'
ROTRIGHT = 'Rotate Right'

# player attributes
START_HEALTH = 9
MAX_HEALTH = 9
MAX_LIVES = 3

# options
# fire options
RADIO_CONTROL = 1
TRACTOR_BEAM = 2
PRESSOR_BEAM  = 3
SCRAMBLER = 4
FIRE_CONTROL = 5
MINI_HOWITZER = 6

# move options
BRAKE = 7
REVERSE_GEAR = 8
FOURTH_GEAR = 9

# during choice
RECOMPILE = 10
CRAB_LEGS = 11
DUAL_PROCESSOR = 12

# during run
ABORT_SWITCH = 13

# after programming
FLYWHEEL = 14
GYRO = 15
CONDITIONAL_PROGRAM = 16

# passive
MECH_ARM = 17
EXTRA_MEMORY = 18
CIRCUIT_BREAKER = 19
REAR_FIRING_LASER = 20
SUPERIOR_ARCHIVE = 21
ABLATIVE_COAT = 22
HIGH_POWERED_LASER = 23
RAMMING_GEAR = 24
DOUBLE_BARRELED_LASER = 25
POWER_DOWN_SHIELD = 26

OPTION_DESC = {
    EXTRA_MEMORY: 'Extra Memory: Get an extra program card at the start of every turn',
#     MECH_ARM: 'Mechanical Arm: Touch flags and repair stations from 1 square away '
#         '(vertically, horizontally, or diagonally)',
    RAMMING_GEAR: 'Ramming Gear: Whenever you bump into another robot (or they bump into you) '
        'they take a damage',
    ABLATIVE_COAT: 'Ablative Coat: This option absorbs 3 damage before you lose it',
    SUPERIOR_ARCHIVE: 'Superior Archive: When you respawn, you respawn on full health, '
        'rather than having taken 2 damage',
    FLYWHEEL: 'Flywheel: Your last program card is your flywheel. It is saved for the next round'
        'as an extra card you may use.',
    CIRCUIT_BREAKER: 'Circuit Breaker: You automatically power down when you have 3 damage taken.',
    DOUBLE_BARRELED_LASER: 'Double Barreled Laser: Shoot with your normal laser twice per turn',
    REAR_FIRING_LASER: 'Rear Firing Laser: Shoot behind you. Cannot be used with double barreled laser',
    POWER_DOWN_SHIELD: 'Power Down Shield: Protects you from up to 1 damage per source per register',
    RECOMPILE: 'Recompile: Once per turn, you may discard all your program cards and get a new hand. '
        'Your robot will then receive one damage.<button id="recompile">Recompile</button>'
}
