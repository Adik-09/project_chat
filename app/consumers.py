# here we are going to implement consumer class by generic websocket consumer [WebsocketConsumer,AsyncWebsocketConsumer].

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import database_sync_to_async
import json  
from .models import *
import base64


class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.user = self.scope["user"]  # To get the name of authenticate user
    print(self.user)
    self.group_name = self.scope['url_route']['kwargs']['room_name']      # to get the group name from url.
        
    if self.user.is_authenticated:
      await self.accept()                      
      await self.channel_layer.group_add(self.group_name,self.channel_name)  # to add the channel to the group
    else:
      await self.close()                      # to diconnect from server we can use self.close()

  async def receive(self, text_data=None, bytes_data=None):

    if text_data:
      data=json.loads(text_data)  # to convert text to python dictionary. this text is comming from client
      print(data)
      if self.user.is_authenticated:
        grp=await database_sync_to_async(Group.objects.get)(grp_name=self.group_name)  # get the group_name instance
      
        chat=chat_message(message=data['msg'],group=grp,author=self.user)     # save group,message,author.
        await database_sync_to_async(chat.save)()
          
        await self.channel_layer.group_send(self.group_name,{                # To send the message to group
          'type':'chat.message',
          'msg': data['msg'],
          'author': self.user.username,
        })

    if bytes_data:
      encoded_data = base64.b64encode(bytes_data).decode('utf-8')
      await self.channel_layer.group_send(self.group_name,{
        'type':'binary.message',
        'file':encoded_data, 
      })
    
  async def binary_message(self,event):
    binary_data = base64.b64decode(event["file"])
    await self.send(bytes_data=binary_data)

  async def chat_message(self,event):                       
    await self.send(text_data=json.dumps(event))             # here you can send data to the client using self.send()

    

  async def disconnect(self, code):
      print(f"{self.user} got disconnected")