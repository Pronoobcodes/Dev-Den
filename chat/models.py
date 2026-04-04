from django.db import models
from django.contrib.auth import get_user_model


class PrivateMessage(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='private_sent_messages')
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='private_received_messages')  
    body = models.TextField()
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.body[:40]}"
