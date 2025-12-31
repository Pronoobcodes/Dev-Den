import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data.get('message', '')
#         username = data.get('username', 'Anonymous')

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'username': username,
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         username = event['username']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username,
#         }))


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return

        # Create a stable room name for the pair (alphabetical)
        users = sorted([self.user.username, self.other_username])
        self.room_group_name = f'pm_{users[0]}_{users[1]}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        body = data.get('message', '').strip()
        if not body:
            return

        sender = self.user.username

        await self.save_private_message(
            self.user.username,
            self.other_username,
            body
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'private_message',
                'message': body,
                'sender': sender,
            }
        )

        await self.send_notification_to_user(
            self.other_username,
            sender,
            body
        )


    async def private_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    @database_sync_to_async
    def save_private_message(self, sender_username, recipient_username, body):
        try:
            sender = User.objects.get(username=sender_username)
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            return None
        from blogApp.models import PrivateMessage
        return PrivateMessage.objects.create(sender=sender, recipient=recipient, body=body)
    
    @database_sync_to_async
    def get_user_id(self, username):
        try:
            return User.objects.get(username=username).id
        except User.DoesNotExist:
            return None

    async def send_notification_to_user(self, recipient_username, sender, message):
        user_id = await self.get_user_id(recipient_username)
        if not user_id:
            return

        await self.channel_layer.group_send(
            f"user_{user_id}",
            {
                "type": "send_notification",
                "message": message,
                "sender": sender,
            }
        )



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close()
            return

        # UNIQUE group per user
        self.group_name = f"user_{user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event.get("sender"),
        }))
