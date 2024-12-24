import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import TBMessages, User, TBRooms
from emoji import demojize

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f'chat_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        response = json.loads(text_data)
        self.save_message(response)
        message = response['message']
        user = response['user']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user
            }
        )

    def chat_message(self, event):
        message = event['message']
        user = event['user']
        self.send(text_data = json.dumps({
            'type': 'chat',
            'message': message,
            'user': user
        }))

    def save_message(self, response):
        TBMessages.objects.create(
            message = demojize(response['message']),
            fkuser = User.objects.get(pk = response['user']),
            fkroom = TBRooms.objects.get(pk = response['room'])
        )