from django.contrib import admin
from .models import News, User
# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date')
class UserAdmin(admin.ModelAdmin):
    list_display = ('studentId', 'email')

admin.site.register(News, NewsAdmin)
admin.site.register(User, UserAdmin)