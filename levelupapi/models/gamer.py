from django.db import models
from django.contrib.auth.models import User

class Gamer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100)
    attending = models.ManyToManyField("Event", through="user_events", related_name="attendees")
    