from django.urls import path

from .consumers import GroupChatConsumer, PersonalChatConsumer


ws_urlpatterns = [
    path("api/chat/group/<group_name>/", GroupChatConsumer.as_asgi(), name="group-chat-ws"),
    path("api/chat/personal/<group_name>/", PersonalChatConsumer.as_asgi(), name="personal-chat-ws"),
]
