# MUST MATCH THE INDEXES IN THE LIST "INDEXES_TO_FILES"
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


SQUARE_SIDES = {
    "b": BLANK,
    "w": WALL,
    "l": LASER1,
    "d": LASER2,
    "t": LASER3,
    "p": PUSHER135,
    "v": PUSHER24
}

SQUARE_CONTENTS = {
    "p": PIT,
    "f": FLOOR,
    "g": GREEN_GEAR,
    "o": RED_GEAR,
    "c": CONVEYER1,
    "x": CONVEYER2,
    "r": REPAIR,
    "h": HAMMER_AND_WRENCH
}

DIRECTIONS = {
    "n": 0,
    "e": 1,
    "s": 2,
    "w": 3
}

FILES = {
    FLOOR: "floor",
    PIT: "pit",
    CONVEYER1: "singleconveyer",
    CONVEYER2: "doubleconveyer",
    GREEN_GEAR: "greengear",
    RED_GEAR: "redgear",
    REPAIR: "repair",
    HAMMER_AND_WRENCH: "hammerwrench",
    BLANK: "empty",
    WALL: "wall",
    LASER1: "singlelaser",
    LASER2: "doublelaser",
    LASER3: "triplelaser",
    PUSHER135: "triplepusher",
    PUSHER24: "doublepusher",
}

INDEXES_TO_FILES = """doubleconveyerconvergeanticlockwise.png
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
wall.png""".split("\n")

FILES_TO_INDEXES = dict([x[::-1] for x in enumerate(INDEXES_TO_FILES)])

TIMEOUT = 20

# GAME SETTINGS
BACKUP = -1,
MOVE1 = 1,
MOVE2 = 2,
MOVE3 = 3,
UTURN = 4,
ROTLEFT = 5,
ROTRIGHT = 6,

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
DOUBLE_BARRELLED_LASER = 25
POWER_DOWN_SHIELD = 26
