from django.db import models
from authentification.models import CustomUser


# Create your models here.

class Room(models.Model):
    room_name = models.CharField(max_length=16, unique=True)
    room_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_rooms")
    members = models.ManyToManyField(CustomUser, related_name="member_rooms")
    request_members = models.ManyToManyField(CustomUser, related_name="rooms_requested")


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.room_owner not in self.members.all():
            self.members.add(self.room_owner)

    def __str__(self):
        return self.room_name

