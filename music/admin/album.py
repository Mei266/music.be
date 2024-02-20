from django.contrib import admin
from music.models import Album, Music

class MuiscInline(admin.TabularInline):
    model = Music

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

    inlines=[
        MuiscInline
    ]


admin.site.register(Album, AlbumAdmin)