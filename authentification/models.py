from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    rooms_owner = models.JSONField(default=list)

    def __str__(self):
        return self.username