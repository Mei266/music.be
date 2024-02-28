from rest_framework import serializers
from music.models import Album, Music
from music.serializers import MusicSerializers

class AlbumSerializers(serializers.ModelSerializer):
    music_list = serializers.SerializerMethodField()
    artist_name = serializers.SerializerMethodField()

    class Meta:
        model = Album
        # fields = "__all__"
        fields = ["id", "title", "artist_name", "image", "image", "music_list"]
        ordering = ["create_at"]

    def get_music_list(self, obj):
        music_list = Music.objects.filter(album=obj.id)
        serializer = MusicSerializers(music_list, many=True)
        return serializer.data
    
    def get_artist_name(self, obj):
        artist = obj.artist.name
        artist_name = [artist]
        return artist_name
