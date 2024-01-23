from django.db import models
from .base import ModelBase

# from django.contrib.postgres.fields import ArrayField
from music.models import Music


class Playlist(ModelBase):
    class Meta:
        verbose_name = "Playlist"
        ordering = ["created_at"]

    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        "music.User", on_delete=models.CASCADE, null=True, blank=True, related_name="playlist_user"
    )
    heart = models.BooleanField(default=False)
    number_of_music = models.IntegerField(default=0)
    # total_time (?)
    image = models.ImageField(upload_to="image/music", null=True)
    description = models.TextField(null=True)
    category = models.ForeignKey(
        "music.Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    musics = models.ManyToManyField(Music, null=True)

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.id:
            super(self.__class__, self).save(*args, **kwargs)
        else:
            self.number_of_music = self.musics.count()
            super(self.__class__, self).save(*args, **kwargs)
