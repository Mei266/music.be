from django.contrib import admin
from music.models import Music


class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Music, MusicAdmin)