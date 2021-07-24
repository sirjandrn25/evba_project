import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# import json



class MechanicNotificationConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        mechanic_id = self.scope['session']['mechanic_id']
        self.room_name = f"mechanic_{mechanic_id}"
        
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
    
    def receive(self,event):
        pass

    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_name,self.channel_name)
    

    def fetch_help(self,event):
        self.send(text_data=json.dumps(event.get('text')))


class DriverNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        driver_id = self.scope['session']['driver_id']
        self.room_name = f"driver_{driver_id}"
       
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
    
    def receive(self,event):
        pass

    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_name,self.channel_name)
    

    def fetch_response(self,event):
        
        self.send(text_data=json.dumps(event.get('text')))