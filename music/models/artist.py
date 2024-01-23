from django.db import models
from .base import ModelBase


class Artist(ModelBase):
    class Meta:
        verbose_name = "Artist"

    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        "music.Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    image = models.ImageField(upload_to="artist", null=False)

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return None
