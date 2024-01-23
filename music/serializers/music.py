from rest_framework import serializers
from music.models import Music


class MusicSerializers(serializers.ModelSerializer):
    artist_name = serializers.SerializerMethodField()

    class Meta:
        model = Music
        # fields = "__all__"
        fields = ["id", "name", "lyric", "heart", "audio", "image", "artist_name"]
        ordering = ["create_at"]

    def get_artist_name(self, obj):
        # Trả về tên của nghệ sĩ từ đối tượng Artist liên quan
        return obj.artist.name


class SearchMusicSerializers(serializers.Serializer):
    search_text = serializers.CharField(required=True)
