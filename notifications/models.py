import json

from django.db import models

from authentification.models import CustomUser


# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")


    def add_message(self, content):
        Message.objects.create(notification=self, content=content)


class Message(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    notification_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content}"

    class Meta:
        ordering = ['-notification_date']