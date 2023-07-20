from channels.generic.websocket import JsonWebsocketConsumer

from asgiref.sync import async_to_sync

import asyncio


from chat.models import Group, ChatMessages


class ChatConsumer(JsonWebsocketConsumer):
    '''
    handel websocket connection of group chatting
    '''

    #constructor
    def __init__(self, *args, **kwargs):
        super().__init__(self, args, kwargs)
        self.user = None
        self.profile_pic = None
        self.group_name = None
        self.group_obj = None


    #connect
    def connect(self):
        #getting the current user
        self.user = self.scope['user']
        self.profile_pic = f"/media/profile_pic/{self.user.profile_pic}"

        #close connection if user is not authenticated
        if not self.user.is_authenticated:
            self.close()

        #getting the dynamic group name(id) set in url
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        
        #get the group instance and close connection if it doesn't exists
        self.group_obj = Group.objects.filter(id=self.group_name).first()

        #close connection if group_obj doesn't exists
        if self.group_obj is None:
            self.close()

        # adding channel layer to group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        #accepting connection
        self.accept() 


    #receive message from client and send to group
    def receive_json(self, context, **kwargs):
        msg = context.get("msg")

        #saving to db
        new_chat = ChatMessages.objects.create(group=self.group_obj, sender=self.user, message=msg)
        new_chat.save()
        chat_time = new_chat.created_at.strftime("%B %d, %Y, %I:%M %p")

        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type": "chat.message",
            "message": msg,
            "user_phone": self.user.phone,
            "user_name": self.user.first_name,
            "user_pic": self.profile_pic,
            "time": str(chat_time),
        })

    #handler to send msg to client when a client send msg to
    def chat_message(self, event):
        self.send_json(event)


    #disconnect
    def disconnect(self, code):
        
        #removing channel from group
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

