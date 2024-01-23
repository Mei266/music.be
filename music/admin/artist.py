from django.contrib import admin
from music.models import Artist


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Artist, ArtistAdmin)