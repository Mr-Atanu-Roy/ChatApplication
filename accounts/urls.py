from django.urls import path

from accounts.views import *


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("contacts/", user_contact, name="contacts"),

]
