from django.urls import path

from api.views import *


urlpatterns = [
    path("search_contact/", search_contact, name="search_contact"),
    path("add_to_contact/", add_to_contact, name="add_to_contact"),
    path("chat_search/", search_chats, name="search_chats"),

    path("group/exit-group/", exit_group, name="exit_group"),
    path("group/delete-group/", delete_group, name="delete_group"),
]
