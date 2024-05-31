from django.contrib import admin
from .models import User, Event
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'createDate')

class EventAdmin(admin.ModelAdmin):
    list_display = ('eventName', 'createUserId', 'createUsername', 'numberOfJoinedUsers')

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
admin.site.register(Event, EventAdmin)