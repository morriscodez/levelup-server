from django.db import models
from django.db.models.deletion import CASCADE


class Event(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    date = models.DateField
    address = models.CharField(max_length=50)
    game = models.ForeignKey("Game", on_delete=CASCADE)
    