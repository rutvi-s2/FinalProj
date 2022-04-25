# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['text']

        print(message)
      
        self.send(text_data=json.dumps({
            'text': message
        }))




# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user_one = self.scope['url_route']['kwargs']['user_one']
        self.user_two = self.scope['url_route']['kwargs']['user_two']
        self.room_name = self.user_one + "." + self.user_two

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

        print("i am getting a message from " + event['user'] + " that says: " + message)
      
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text': message,
            'user': event['user']
        }))