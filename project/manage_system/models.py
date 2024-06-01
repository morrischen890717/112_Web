from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Event(models.Model):
    eventName = models.CharField(max_length=150)
    eventDateTime = models.DateTimeField()
    createUser = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name = 'createdEvents')
    joinedUsers = models.ManyToManyField(User, related_name='joinedEvents', blank=True)
    max_limit = models.PositiveIntegerField()
    createDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-createDate',)

    def __str__(self):
        return self.eventName
