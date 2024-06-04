from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Event
# Register your models here.

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'createDate', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    list_display = ('username', 'email', 'is_staff', 'createDate')
    search_fields = ('username', 'email')
    ordering = ('-createDate',)

class EventAdmin(admin.ModelAdmin):
    # list_display = ('eventName', 'eventDateTime', 'createUserId', 'createUsername', 'numberOfJoinedUsers')
    list_display = ('eventName', 'createDate')

    def createUserId(self, obj):
        return obj.createUser.id
    createUserId.short_description = 'Creator ID' # setting title

    def createUsername(self, obj):
        return obj.createUser.username
    createUsername.short_description = 'Creator Username' # setting title

    def numberOfJoinedUsers(self, obj):
        return obj.joinedUsers.count()
    numberOfJoinedUsers.short_description = '# of Participants' # setting title

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Event, EventAdmin)