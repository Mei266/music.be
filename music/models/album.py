from django.db import models
from .base import ModelBase
from music.models import Music


class Album(ModelBase):
    class Meta:
        verbose_name = "Album"

    title = models.CharField(max_length=100)
    artist = models.ForeignKey("music.Artist", on_delete=models.PROTECT)
    image = models.ImageField(upload_to="album")

    def __str__(self):
        return '%s - %s' % (self.pk, self.title)

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return None
