from django.urls import path

from chat.views import *


urlpatterns = [
    path("", chat_home, name="home"),
    path("new-chat/group/", new_chat_group, name="new-chat-group"),
    path("chat/group/<id>", chat_group, name="chat-group"),
    path("settings/group/<id>", chat_group_settings, name="chat-group-settings"),

]
