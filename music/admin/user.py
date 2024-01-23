from django.contrib import admin
from music.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(User, UserAdmin)