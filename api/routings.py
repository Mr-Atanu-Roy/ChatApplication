from django.urls import path

from .consumers import ChatConsumer


ws_urlpatterns = [
    path("api/chat/group/<group_name>/", ChatConsumer.as_asgi(), name="group-chat-ws"),
]
