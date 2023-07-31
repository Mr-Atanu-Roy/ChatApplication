from django.contrib import admin

from accounts.models import User, UserContacts, Notification, FriendRequests

# Register your models here.

class UserContactsInline(admin.TabularInline):
    model = UserContacts
    extra = 0
    classes = ['collapse']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'first_name', 'last_login', 'is_staff')
    fieldsets = [
        ("User Details", {
            "fields": (
                ['profile_pic', 'phone', 'email', 'password', 'first_name', 'last_name']
            ),
        }),
        ("More Details", {
            "fields": (
                ['date_joined', 'last_login', 'last_logout']
            ), 'classes': ['collapse']
        }),
        ("Permissions", {
            "fields": (
                ['is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups']
            ), 'classes': ['collapse']
        }),
    ]

    inlines = [UserContactsInline]


    
    
@admin.register(UserContacts)
class UserContactsAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    fieldsets = [
        ("User Contacts Details", {
            "fields": (
                ['user', 'contacts']
            ),
        }),
    ]


@admin.register(FriendRequests)
class FriendRequestsAdmin(admin.ModelAdmin):
    list_display = ('request_for', 'request_from', 'status', 'created_at', 'updated_at')
    fieldsets = [
        ("Details", {
            "fields": (
                ['request_for', 'request_from', 'status']
            ),
        }),
    ]
    
    
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_for', 'notification_type', 'seen', 'created_at', 'updated_at')
    fieldsets = [
        ("Notification Details", {
            "fields": (
                ['notification_for', 'notification_type', 'seen', 'message']
            ),
        }),
    ]
    
    