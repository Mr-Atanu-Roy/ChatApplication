from channels.generic.websocket import JsonWebsocketConsumer

from asgiref.sync import async_to_sync


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
        self.profile_pic = f"/media/{self.user.profile_pic}"

        #close connection if user is not authenticated
        if not self.user.is_authenticated:
            self.close()
            return

        #getting the dynamic group name(id) set in url
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        
        #get the group instance and close connection if it doesn't exists
        self.group_obj = Group.objects.filter(id=self.group_name).first()

        #close connection if group_obj doesn't exists
        if self.group_obj is None:
            self.close()
            return

        #accepting connection
        self.accept()

        # adding channel layer to group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        #send list of online users to newly joined user
        online_users = self.group_obj.online.all()
        self.send_json({
            "type": "user.list",
            "online_num": len(online_users),
            "online_users": [users.first_name for users in online_users]
        })

        #send message to other users when a new user joins
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type": "user.join",
            "phone": self.user.phone,
            "username": self.user.first_name,
        })

        #adding user to online field: added in end so that users dont see them as online 
        self.group_obj.online.add(self.user)


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

    #handler to send msg when a user comes online
    def user_join(self, event):
        self.send_json(event)

    #handler to send msg when a user leaves
    def user_leave(self, event):
        self.send_json(event)


    #disconnect
    def disconnect(self, code):

        #remove from online field of group
        self.group_obj.online.remove(self.user)

        #send msg when user leave
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type": "user.leave",
            "phone": self.user.phone,
            "username": self.user.first_name,
        })
        
        #removing channel from group
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

