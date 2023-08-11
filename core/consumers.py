import json
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom,Message
from django.db.models import Q
from django.contrib.auth import get_user_model

User=get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'
        self.room_group_name = 'chat_%s' % self.room_name
        user_list=[my_id,other_user_id]
        await self.save_chat_room(self.room_group_name,user_list)
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()
        # room=await self.get_room(self.room_group_name)
        # username=await self.get_user_id(my_id)
        # message_data=await self.get_room_chat(room)
        # await self.send(text_data=json.dumps({"message": [message_data],"username":username}))
        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username=text_data_json["username"]
        receiver=text_data_json["receiver"]
        message_type=text_data_json['type']
        # Send message to room group
        room=await self.get_room(self.room_group_name)
        if message_type=="chat_message":

            sender=await self.get_user(username)
            receivers=await self.get_user(receiver)
            
            await self.save_messages(room,sender,receivers,message)
        
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message,"username":username}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username=event["username"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,"username":username}))

    @database_sync_to_async
    def get_user_id(self,id):
        return User.objects.get(id=id)
    @database_sync_to_async
    def get_user(self,name):
        return User.objects.get(username=name)
    @database_sync_to_async
    def get_room(self,room):
        return ChatRoom.objects.get(name=room)
    @database_sync_to_async
    def get_room_chat(self,room_name):
        return Message.objects.filter(room=room_name)
    @database_sync_to_async
    def save_chat_room(self,name,users):
        model=User.objects.filter(id__in=users)
        chat_room=ChatRoom.objects.filter(Q(users__in=model) & Q(name=name))
        if chat_room:
            pass
        else:
            data=ChatRoom.objects.create(name=name)
            data.users.add(*model)
    @database_sync_to_async
    def save_messages(self,room,sender,receiver,message):
        
        print(sender,receiver,room)
        Message.objects.create(
            from_user=sender,
            messages=message,
            to_user=receiver,
            room=room)
        print('Done')
    
    def messages_to_json():
        pass
