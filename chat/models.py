from django.db import models

from accounts.models import User
from accounts.utils import BaseModel


#choices
msg_type_choices = (
    ("text", "Text"),
    ("link", "Link"),
    ("img", "Image"),
    ("audio", "Audio"),
    ("video", "Video"),
    ("doc", "Document"),      
)



# Create your models here.

class Group(BaseModel):
    name = models.CharField(max_length=650)
    description = models.CharField(max_length=500, null=True, blank=True, default="")
    group_pic = models.FileField(max_length=355, blank=True, null=True, upload_to="group_pic/", default="group_pic/default_group_pic.jpg")
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='created_group')
    members = models.ManyToManyField(User)
    type = models.CharField(default="group", choices=(("personal", "Personal"), ("group", "Group")), max_length=255)

    #for tracking who are online
    online = models.ManyToManyField(User, related_name='online')

    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name_plural = "Conversat Groups"
        ordering = ['-created_at']
    


class ChatMessages(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.CharField(max_length=650, blank=True, null=True)
    message_type = models.CharField(choices=msg_type_choices, default="text", max_length=255)
    file = models.FileField(upload_to="chats/file/", null=True, blank=True, max_length=655)
    file_ext = models.CharField(blank=True, null=True, max_length=255)
    file_name = models.CharField(null=True, blank=True, max_length=655)
    file_size = models.CharField(default="0", max_length=255)

    def __str__(self):
        return f"{self.sender}/{self.message_type}"



