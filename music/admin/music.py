from django.contrib import admin
from music.models import Music, ArtistItem
from django import forms


class ArtistInline(admin.TabularInline):
    model = ArtistItem


class MusicAdminForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = '__all__'
        widgets = {
            'duration': forms.HiddenInput(), # Ẩn trường time_of_music
            'number_listens': forms.HiddenInput(), # Ẩn trường time_of_music
        }

class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration', 'number_listens')
    form = MusicAdminForm
    inlines = [ ArtistInline ]


admin.site.register(Music, MusicAdmin)