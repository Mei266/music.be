from django.contrib import admin
from music.models import Music, ArtistItem

class ArtistInline(admin.TabularInline):
    model = ArtistItem

class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    inlines = [ ArtistInline ]


admin.site.register(Music, MusicAdmin)