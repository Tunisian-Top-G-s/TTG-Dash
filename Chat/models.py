#Chat/models.py

from django.db import models

from Users.models import CustomUser

# Create your models here.

class Section(models.Model):
    index = models.IntegerField(default=0)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Room(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='rooms', null=True, blank=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=10000)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)  # Add this field
    timestamp = models.DateTimeField(auto_now_add=True)