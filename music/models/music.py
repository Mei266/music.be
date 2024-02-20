from django.db import models
from .base import ModelBase


class Music(ModelBase):
    class Meta:
        verbose_name = "Music"
        ordering = ["created_at"]

    name = models.CharField(max_length=100)
    lyric = models.TextField()
    artist = models.ManyToManyField("music.Artist", related_name="artist_item", through='ArtistItem')
    album = models.ForeignKey(
        "music.Album", on_delete=models.PROTECT, null=True, blank=True
    )
    audio = models.FileField(upload_to="audio", null=False)
    image = models.ImageField(upload_to="image/music", null=False)
    number_listens = models.IntegerField(default=0)

    popular = models.BooleanField(default=False)

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

class ArtistItem(ModelBase):
    artist = models.ForeignKey("music.Artist", on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ArtistItem"
        ordering = ["created_at"]
