from django.urls import path

from accounts.views import *


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),

    path("last_seen/update", last_seen, name="last_seen"),

]
