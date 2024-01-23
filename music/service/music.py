from backend.service import ServiceBase
from backend.models import Music
from django.db.models import F


class MusicService(ServiceBase):
    def __init__(self):
        pass

    def get_all(self):
        musics = Music.objects.all().annotate(artist=F("artist__name"))
        return musics


music_service = MusicService()
