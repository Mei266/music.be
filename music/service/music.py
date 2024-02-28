from music.service import ServiceBase
from music.models import Music
from django.db.models import F
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC


class MusicService(ServiceBase):
    def __init__(self):
        pass

    def get_all(self):
        musics = Music.objects.all().annotate(artist=F("artist__name"))
        return musics
    
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


music_service = MusicService()
