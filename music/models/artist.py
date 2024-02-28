from django.db import models
from .base import ModelBase


class Artist(ModelBase):
    class Meta:
        verbose_name = "Artist"

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="artist", null=False)

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return None

    def __str__(self):
        return '%s - %s' % (self.pk, self.name)