from django.db import models
from django.utils.six import with_metaclass
from game_settings import *

INF = 1<<15

class ListField(with_metaclass(models.SubfieldBase, models.CharField)):
    def __init__(self, seps, datatype, *args, **kwargs):
        self.seps = seps
        self.datatype = datatype
        kwargs['max_length'] = INF
        super(ListField, self).__init__(*args, **kwargs)
    def get_prep_value(self, value):
        firstlayer = not hasattr(self, 'depth')
        if firstlayer:
            self.depth = 0
        else:
            self.depth += 1
        if isinstance(value, list):
            value = self.seps[self.depth].join(self.get_prep_value(x) for x in value)
            self.depth -= 1
            if firstlayer:
                del self.depth
            return value
        else:
            self.depth -= 1
            return str(value)

    def to_python(self, value):
        if value == '': return []
        firstlayer = not hasattr(self, 'depth')
        if firstlayer:
            self.depth = 0
        else:
            self.depth += 1
        if self.depth < len(self.seps):
            value = [self.to_python(x) for x in value.split(self.seps[self.depth])]
            self.depth -= 1
            if firstlayer:
                del self.depth
            return value
        else:
            self.depth -= 1
            return self.datatype(value)

class Square():
    def __init__(self, contents):
        self.walls = []
        square, walls = contents[:-4], contents[-4:]
        for side in walls:
            self.walls.append(SQUARE_SIDES[side])
        self.square = SQUARE_CONTENTS[square[0]]


        self.file = FILES[self.square]
        self.rotation = 0

        if self.square in [CONVEYER1, CONVEYER2]:
            self.exit = DIRECTIONS[square[1]]
            self.entrances = [DIRECTIONS[way] for way in square[2:]]
            self.rotation = self.exit * 90

            if self.square == CONVEYER1:
                self.file = "singleconveyer"
            else:
                self.file = "doubleconveyer"

            if len(self.entrances) == 1:
                if (self.entrances[0] + self.exit) % 2 == 0:
                    self.file += "straight"
                elif (self.entrances[0] + 1) % 4 == self.exit:
                    self.file += "turnanticlockwise"
                else:
                    self.file += "turnclockwise"
            else:
                self.file += "converge"
                if (self.entrances[0] + self.exit) % 2 == 0:
                    self.entrances.pop(0)
                elif (self.entrances[1] + self.exit) % 2 == 0:
                    self.entrances.pop(1)
                if len(self.entrances) == 2:
                    pass # just normal converge
                elif (self.entrances[0] + 1) % 4 == self.exit:
                    self.file += "anticlockwise"
                else:
                    self.file += "clockwise"
        self.file += ".png"

    def tojs(self):
        img = FILES_TO_INDEXES[self.file]
        return ",".join(map(str, [img, self.rotation] + self.walls))


class Course(models.Model):
    filename = models.FilePathField(primary_key=True)
    name = models.CharField(max_length=INF)
    description = models.CharField(max_length=INF)
    rules = ListField([' '], str)
    rules_description = models.CharField(max_length=INF)
    length = models.CharField(max_length=INF)
    difficulty = models.CharField(max_length=INF)
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    spawn = ListField([' ', ','], int)
    flags = ListField([' ', ','], int)
    board = ListField(['\n', ' '], Square)
