from django.contrib import admin
from music.models import Playlist, PlaylistItem

class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    inlines = [ PlaylistItemInline ]


admin.site.register(Playlist, PlaylistAdmin)