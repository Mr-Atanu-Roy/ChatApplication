from django.contrib import admin

from accounts.models import User, UserContacts

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
    
    
    
    