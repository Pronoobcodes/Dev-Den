from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class ChatMessage(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    room_name = models.CharField(max_length=255)
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.timestamp}] {self.sender}: {self.message}'