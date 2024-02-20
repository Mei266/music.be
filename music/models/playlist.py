from django.db import models
from .base import ModelBase



class Playlist(ModelBase):
    class Meta:
        verbose_name = "Playlist"
        ordering = ["created_at"]

    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        "music.User", on_delete=models.CASCADE, null=True, blank=True, related_name="playlist_user"
    )
    heart = models.BooleanField(default=False)
    image = models.ImageField(upload_to="image/music", null=True)
    description = models.TextField(null=True)
    musics = models.ManyToManyField(
        "music.Music", related_name="playlist_item", through='PlaylistItem'
    )

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return None

class PlaylistItem(ModelBase):
    playist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    music = models.ForeignKey("music.Music", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Playlistitem"
        ordering = ["created_at"]