from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

class User_Event(models.Model):

    event = models.ForeignKey("Event", on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
