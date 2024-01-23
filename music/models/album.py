from django.db import models
from .base import ModelBase
from music.models import Music


class Album(ModelBase):
    class Meta:
        verbose_name = "Album"

    title = models.CharField(max_length=100)
    artist = models.ForeignKey("music.Artist", on_delete=models.RESTRICT)
    heart = models.BooleanField(default=False)
    number_of_music = models.IntegerField(default=0)
    image = models.ImageField(upload_to="album")
    category = models.ForeignKey(
        "music.Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    musics = models.ManyToManyField(Music)

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return None
