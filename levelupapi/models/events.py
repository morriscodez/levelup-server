from django.db import models
from django.db.models.deletion import CASCADE


class Event(models.Model):

    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateTimeField()
    address = models.CharField(max_length=50)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", through="User_Event", related_name="attending")
    time = models.TimeField()

    @property
    def joined(self):
        return self.__joined

    