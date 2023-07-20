from django.urls import path

from api.views import *


urlpatterns = [
    path("search_contact_ajax/", search_contact_ajax, name="search_contact_ajax"),
    path("add_to_user_contact/", add_to_user_contact, name="add_to_user_contact"),
]
