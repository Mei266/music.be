from django.contrib import admin
from music.models import Artist, Music

class MuiscInline(admin.TabularInline):
    model = Music.artist.through


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [ MuiscInline ]


admin.site.register(Artist, ArtistAdmin)