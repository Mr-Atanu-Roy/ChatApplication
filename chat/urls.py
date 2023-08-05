from django.urls import path

from chat.views import *
from accounts.views import profile, user_contact, notifications


urlpatterns = [
    path("", chat_home, name="home"),
    
    path("new-chat/group/", new_chat_group, name="new-chat-group"),
    path("chat/group/<id>", chat_group, name="chat-group"),
    path("settings/group/<id>", chat_group_settings, name="chat-group-settings"),

    path("chat/personal/p/<user_id>", chat_personal_get, name="chat-personal-get"),
    path("chat/personal/<id>", chat_personal, name="chat-personal"),

    #views from accounts app
    path("profile/", profile, name="profile"),
    path("friends/", user_contact, name="contacts"),
    path("notifications/", notifications, name="notifications"),

]
