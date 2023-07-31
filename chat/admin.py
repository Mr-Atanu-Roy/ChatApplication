from django.contrib import admin

from chat.models import ChatMessages, Group

# Register your models here.


class ChatMessagesInline(admin.TabularInline):
    model = ChatMessages
    extra = 0
    classes = ['collapse']
    

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'type', 'created_at')
    fieldsets = [
        ("Group Details", {
            "fields": (
                ['name', 'owner', 'type', 'group_pic']
            ),
        }),
        ("More Details", {
            "fields": (
                ['description', 'members']
            ), 'classes': ['collapse']
        }),
    ]

    inlines = [ChatMessagesInline]
    
    
    
@admin.register(ChatMessages)
class ChatMessagesAdmin(admin.ModelAdmin):
    list_display = ('group', 'sender', 'message_type', 'created_at')
    fieldsets = [
        ("Message Details", {
            "fields": (
                ['group', 'sender', 'message_type', 'message', 'file']
            ),
        }),
         ("More Details", {
            "fields": (
                ['file_name', 'file_ext', 'file_size']
            ), 'classes': ['collapse']
        }),
    ]
