from channels.generic.websocket import JsonWebsocketConsumer

from asgiref.sync import async_to_sync

from chat.models import Group, ChatMessages


class GroupChatConsumer(JsonWebsocketConsumer):
    '''
    handel websocket connection of group chatting
    '''

    #constructor
    def __init__(self, *args, **kwargs):
        super().__init__(self, args, kwargs)
        self.user = None            #current user instance
        self.profile_pic = None     #current user profile pic
        self.group_name = None      #dynamic group name(id set in url)
        self.group_obj = None       #group obj


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
        self.group_obj = Group.objects.filter(id=self.group_name).select_related().first()

        #close connection if group_obj doesn't exists
        if self.group_obj is None:
            self.close()
            return

        #accepting connection
        self.accept()

        # adding channel layer to group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        #adding user to online field
        self.group_obj.online.add(self.user)

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


    #receive message from client and send to group
    def receive_json(self, context, **kwargs):
        msg_type = context.get("msg_type")

        #for text messages
        if msg_type == "text":
            #get the text message
            msg = context.get("msg").strip()
            
            #check if msg is blank
            if msg != "":

                #saving msg to db
                new_chat = ChatMessages.objects.create(group=self.group_obj, sender=self.user, message=msg)
                new_chat.save()
                chat_time = new_chat.created_at.strftime("%B %d, %Y, %I:%M %p")

                async_to_sync(self.channel_layer.group_send)(self.group_name, {
                    "type": "chat.message",
                    "msg_type": msg_type,
                    "message": msg,
                    "user_phone": self.user.phone,
                    "user_name": self.user.first_name,
                    "user_pic": self.profile_pic,
                    "time": str(chat_time),
                })


        #for file message
        elif msg_type == "file":

            async_to_sync(self.channel_layer.group_send)(self.group_name, {
                "type": "chat.message",
                "msg_type": msg_type,
                "message": context.get("files", []),
                "user_phone": self.user.phone,
                "user_name": self.user.first_name,
                "user_pic": self.profile_pic,
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

        #remove from online field of group when he exit
        self.group_obj.online.remove(self.user)

        #send msg when user leave
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type": "user.leave",
            "phone": self.user.phone,
            "username": self.user.first_name,
        })
        
        #removing channel from group
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)




class PersonalChatConsumer(JsonWebsocketConsumer):
    '''
    handel websocket connection of personal chatting
    '''


    #constructor
    def __init__(self, *args, **kwargs):
        super().__init__(self, args, kwargs)
        self.user = None            #current user instance
        self.group_name = None      #dynamic group name(id set in url)
        self.group_obj = None       #group obj


    #connect
    def connect(self):
        #getting the current user
        self.user = self.scope['user']

        #close connection if user is not authenticated
        if not self.user.is_authenticated:
            self.close()
            return
        
        #getting the dynamic group name(id) set in url
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        #get the group instance and close connection if it doesn't exists
        self.group_obj = Group.objects.filter(id=self.group_name).select_related().first()

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
        last_seen = ""

        try:
            if len(online_users) == 0:
                other_user = self.group_obj.members.exclude(pk=self.user.pk).first()
                last_seen = other_user.last_login.strftime("%B %d, %Y, %I:%M %p")
        except Exception as e:
            print(e) 
            pass

        self.send_json({
            "type": "user.list",
            "online_num": len(online_users),
            "last_seen": last_seen,
        })

        #send message to other users when a new user joins
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type": "user.join",
            "phone": self.user.phone,
        })

        #adding user to online field
        self.group_obj.online.add(self.user)


    
    #receive message from client and send to group
    def receive_json(self, context, **kwargs):
        msg_type = context.get("msg_type")

        #for text messages
        if msg_type == "text":
            #getting the text msg
            msg = context.get("msg").strip()

            #check if msg is blank
            if msg != "":

                #saving msg to db
                new_chat = ChatMessages.objects.create(group=self.group_obj, sender=self.user, message=msg)
                new_chat.save()
                chat_time = new_chat.created_at.strftime("%B %d, %Y, %I:%M %p")

                async_to_sync(self.channel_layer.group_send)(self.group_name, {
                    "type": "chat.message",
                    "msg_type": msg_type,
                    "message": msg,
                    "user_phone": self.user.phone,
                    "time": chat_time,
                })

            
        #for file messages
        elif msg_type == "file":

            async_to_sync(self.channel_layer.group_send)(self.group_name, {
                "type": "chat.message",
                "msg_type": msg_type,
                "message": context.get("files", []),
                "user_phone": self.user.phone,
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

        #remove from online field of group when he exit
        self.group_obj.online.remove(self.user)

        #send msg when user leave
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type": "user.leave",
            "phone": self.user.phone,
            "last_seen": self.user.last_login.strftime("%B %d, %Y, %I:%M %p")
        })
        
        #removing channel from group
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)


