from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    telegramId = models.TextField(blank = True)
    emailPassword = models.TextField(blank = True)
    reqCount = models.IntegerField()
    def __str__(self):
        return f"{self.username}"
