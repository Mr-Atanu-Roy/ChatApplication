from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.utils import BaseModel, cache_delete
from accounts.manager import Usermanager

import uuid


#choices
notification_type_choices = (
    ("personal", "personal"),
    ("group", "Group"),
    ("application", "Application"),
)




# Create your models here.

#custom user model
class User(AbstractUser):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    username = None
    phone = models.CharField(unique=True, max_length=15)
    email = models.EmailField(blank=True, null=True, default="")
    profile_pic = models.FileField(max_length=355, blank=True, null=True, upload_to="profile_pic/")
    last_logout = models.DateTimeField(null=True, blank=True)
    
    objects = Usermanager()
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'auth_user'
        verbose_name_plural = "Conversat User"
        ordering = ['date_joined']
    
    def __str__(self):
        return self.phone
    



class UserContacts(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_contact')
    contacts = models.ManyToManyField(User)

    def __str__(self):
        return str(self.user)
    
    
    class Meta:
        verbose_name_plural = "User Contacts"
        ordering = ['created_at']



class Notification(BaseModel):
    message = models.CharField(max_length=655)
    notification_type = models.CharField(choices=notification_type_choices, max_length=255)
    notification_for = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.notification_for)
    

class FriendRequests(BaseModel):
    request_for = models.ForeignKey(User, on_delete=models.CASCADE)
    request_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_request")
    message = models.CharField(max_length=355, null=True, blank=True)
    status = models.BooleanField(default=False) #True->accepted False->Declined
    seen = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.request_for)
    
    class Meta:
        verbose_name_plural = "Friend Requests"

