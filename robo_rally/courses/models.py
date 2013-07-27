from django.db import models

INF = 1<<15

class IntListField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = INF
        super(IntListField, self).__init__(*args, **kwargs)
    def get_prep_value(self, value):
        return " ".join(map(str, value))

    def to_python(self, value):
        return map(int, value.split(' '))

class Course(models.Model):
    filename = models.FilePathField(primary_key=True)
    name = models.CharField(max_length=INF)
    description = models.CharField(max_length=INF)
    rules = models.CharField(max_length=INF)
    rules_description = models.CharField(max_length=INF)
    length = models.CharField(max_length=INF)
    difficulty = models.CharField(max_length=INF)
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    spawn = IntListField()
    flags = IntListField()
    board = models.CharField(max_length=INF)
