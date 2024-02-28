from django.db import models
from .base import ModelBase
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
import os
from mysite.settings import MEDIA_ROOT

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
    duration = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.pk, self.name)

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
    
    def get_audio_duration(self, file_path):
        try:
            if file_path.endswith('.mp3'):
                audio = MP3(file_path)
            elif file_path.endswith('.ogg'):
                audio = OggVorbis(file_path)
            elif file_path.endswith('.flac'):
                audio = FLAC(file_path)
            else:
                return None  # Unsupported file format
            duration_seconds = audio.info.length
            duration_minutes = int(duration_seconds // 60)
            duration_seconds = int(duration_seconds % 60)
            return f"{duration_minutes}:{duration_seconds:02d}"
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_absolute_file_path(self, file_url):
        # Xóa '/media/' khỏi đường dẫn URL để lấy phần còn lại
        relative_path = file_url.replace('/media/', '')

        # Kết hợp đường dẫn tuyệt đối của MEDIA_ROOT với phần còn lại của đường dẫn
        absolute_path = os.path.join(MEDIA_ROOT, relative_path)

        return absolute_path

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        path = self.get_absolute_file_path(self.audio_url())
        self.duration = self.get_audio_duration(path)
        super().save(*args, **kwargs)

class ArtistItem(ModelBase):
    artist = models.ForeignKey("music.Artist", on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ArtistItem"
        ordering = ["created_at"]

class Heart(ModelBase):
    user = models.ForeignKey("music.User", on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Heart"
        ordering = ["created_at"]