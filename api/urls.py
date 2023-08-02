from django.urls import path

from api.views import *


urlpatterns = [
    path("search_contact/", search_contact, name="search_contact"),
    path("add_to_contact/", add_to_contact, name="add_to_contact"),
    path("chat_search/", search_chats, name="search_chats"),

    path("group/exit-group/", exit_group, name="exit_group"),
    path("group/delete-group/", delete_group, name="delete_group"),

    path("msg/upload-file/", upload_msg_file, name="upload_msg_file"),

    path("notifications/load/", load_notification, name="load_notification"),
    path("friend_requests/load/", load_friend_requests, name="load_friend_requests"),
    path("friend_requests/accept/", accept_friend_requests, name="accept_friend_requests"),
    path("friend_requests/decline/", decline_friend_requests, name="decline_friend_requests"),
]
