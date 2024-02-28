from rest_framework import serializers
from music.models import Music


class MusicSerializers(serializers.ModelSerializer):
    artist_name = serializers.SerializerMethodField()
    album_name = serializers.SerializerMethodField()

    class Meta:
        model = Music
        # fields = "__all__"
        fields = ["id", "name", "lyric", "audio", "image", "artist_name", "duration", "number_listens", "album_name"]
        ordering = ["create_at"]

    def get_artist_name(self, obj):
        # Trả về tên của nghệ sĩ từ đối tượng Artist liên quan
        return list(obj.artist.values_list('name', flat=True))
    
    def get_album_name(self, obj):
        # Trả về tên của nghệ sĩ từ đối tượng Artist liên quan
        if obj.album:
            return obj.album.title
        return None


class SearchMusicSerializers(serializers.Serializer):
    search_text = serializers.CharField(required=True)
