from rest_framework import serializers
from music.models import Artist
from music.serializers import MusicSerializers


class ArtistSerializers(serializers.ModelSerializer):
    music_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Artist
        fields = ["id","name", "image", "music_list"]
        ordering = ["create_at"]
    
    def get_music_list(self, obj):
        artist = Artist.objects.get(pk=obj.id)
        music_list = artist.artist_item.all()
        serializer = MusicSerializers(music_list, many=True)
        return serializer.data
