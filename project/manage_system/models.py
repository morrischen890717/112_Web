from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
# Create your models here.

# class User(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=50)
#     createDate = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.username

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    createDate = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Event(models.Model):
    eventName = models.CharField(max_length=150)
    eventDateTime = models.DateTimeField(null=True)
    createUser = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name = 'createdEvents')
    joinedUsers = models.ManyToManyField(User, related_name='joinedEvents', blank=True)
    max_limit = models.PositiveIntegerField(null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    sheetId = models.CharField(max_length=150, null=True)
    draftId = models.CharField(max_length=150, null=True)

    class Meta:
        ordering=('-createDate',)

    def __str__(self):
        return self.eventName

