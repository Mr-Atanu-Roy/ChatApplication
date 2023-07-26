from channels.generic.websocket import JsonWebsocketConsumer

from asgiref.sync import async_to_sync

from chat.models import Group, ChatMessages
from accounts.utils import cache_get, cache_set, cache_delete


class ChatConsumer(JsonWebsocketConsumer):
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
        self.cache_key = None       #for cache 


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

        self.cache_key = f"ws_grp_online_mem_{self.group_name}"

        #adding newly joined user to cached data
        #get the cached data
        cached_data = cache_get(self.cache_key)

        #check if cache exists: if exists then someone else id online
        if cached_data:
            #add the user to cached data
            cached_data[f"{self.user}"] = f"{self.user.first_name}"
            cache_delete(self.cache_key)
            cache_set(self.cache_key, cached_data)
        else:
            #no one online: create cached data
            cached_data = {
                f"{self.user}": f"{self.user.first_name}"
            }
            #set cached data
            cache_set(self.cache_key, cached_data)

        #send list of online users to newly joined user
        self.send_json({
            "type": "user.list",
            "online_num": 0 if cached_data==None else len(cached_data),
            "online_users": [] if cached_data==None else [users for users in cached_data]
        })

        #send message to other users when a new user joins
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type": "user.join",
            "phone": self.user.phone,
            "username": self.user.first_name,
        })


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

        #removing user from cached data when he exits
        #get cached data
        cached_data = cache_get(self.cache_key)

        #check if cached data exists
        if cached_data:
            #remove the user from cached data
            cached_data.pop(f"{self.user}", None)
            #delete the cache
            cache_delete(self.cache_key)
            #set the cache only if someone else is online
            if len(cached_data) > 0:
                cache_set(self.cache_key, cached_data)


        #send msg when user leave
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type": "user.leave",
            "phone": self.user.phone,
            "username": self.user.first_name,
        })
        
        #removing channel from group
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

