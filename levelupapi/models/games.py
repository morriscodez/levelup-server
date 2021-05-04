from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField


class Game(models.Model):

    user = models.ForeignKey(User, on_delete=CASCADE)
    label = CharField(max_length=50)
    game_type = models.ForeignKey("Game_Type", on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
