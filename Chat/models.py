#Chat/models.py

from django.db import models

from Users.models import CustomUser

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)
    