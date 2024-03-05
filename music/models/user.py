from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField("image/user", null=True, blank=True)
    hearts = models.ManyToManyField("music.Music", related_name="user_heart")
    follows = models.ManyToManyField("music.Artist", related_name="user_follow")

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return None
