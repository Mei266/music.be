from django.contrib import admin
from music.models import Playlist


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Playlist, PlaylistAdmin)