from django.contrib import admin
from music.models import Album, Music
from music.admin.music import MusicAdminForm

class MuiscInline(admin.TabularInline):
    model = Music
    form = MusicAdminForm

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

    inlines=[
        MuiscInline
    ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        obj = form.instance
        for instance in instances:
            # Do something with `instance`
            instance.save()
            instance.artist.add(obj.artist)
        formset.save_m2m()


admin.site.register(Album, AlbumAdmin)