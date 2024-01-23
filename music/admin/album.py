from django.contrib import admin
from music.models import Album


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Album, AlbumAdmin)