from django.db import models
from .base import ModelBase


class Music(ModelBase):
    class Meta:
        verbose_name = "Music"
        ordering = ["created_at"]

    name = models.CharField(max_length=100)
    lyric = models.TextField()
    artist = models.ForeignKey("music.Artist", on_delete=models.RESTRICT)
    # album = models.ForeignKey(
    #     "backend.Album", on_delete=models.SET_NULL, null=True, blank=True
    # )
    # playlist = models.ForeignKey(
    #     "backend.Playlist", on_delete=models.SET_NULL, null=True, blank=True
    # )
    heart = models.BooleanField(default=False)
    audio = models.FileField(upload_to="audio", null=False)
    image = models.ImageField(upload_to="image/music", null=False)

    def audio_url(self):
        if self.audio:
            return self.audio.url
        else:
            return None

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return None
