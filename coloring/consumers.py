# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user_one = self.scope['url_route']['kwargs']['user_one']
        self.user_two = self.scope['url_route']['kwargs']['user_two']
        self.room_name = self.user_one + "." + self.user_two
        ### TODO: Get associated chat storage
        self.chat_storage = ChatStorage.objects.filter(user_one=self.user_one, user_two=self.user_two)
        if not self.chat_storage:
          self.chat_storage = ChatStorage(user_one=self.user_one, user_two=self.user_two)
          self.chat_storage.save()
        else:
          self.chat_storage = ChatStorage.objects.get(user_one=self.user_one, user_two=self.user_two)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['text']


        print("i am getting a message from " + text_data_json['user'] + " that says: " + message)
        #### STORE ME IN A MODEL CHATSTORAGE PLS
      
        from_user_temp = text_data_json['user']
        to_user_temp = self.user_one if from_user_temp is self.user_two else self.user_two
        new_msg = Message(text=message, from_user=from_user_temp, to_user=to_user_temp, chat_storage=self.chat_storage)
        new_msg.save()

      
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'text': message,
                'user': text_data_json['user']
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['text']
      
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text': message,
            'user': event['user']
        }))