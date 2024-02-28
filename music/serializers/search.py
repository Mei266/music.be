from rest_framework import serializers
from music.models import Album, Music
from music.serializers import MusicSerializers, AlbumSerializers, ArtistSerializers

class SearchSerializers(serializers.Serializer):
    musics = MusicSerializers(required=False, read_only=True, source='*', many=True)
    artists = ArtistSerializers(required=False, read_only=True, source='*', many=True)
    albums = AlbumSerializers(required=False, read_only=True, source='*', many=True)

