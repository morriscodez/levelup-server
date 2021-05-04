from django.db import models
from django.db.models.deletion import CASCADE


class Event(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateTimeField()
    address = models.CharField(max_length=50)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", through="User_Event", related_name="attending")
    