from rest_framework import serializers
from music.models import Playlist
from music.serializers import MusicSerializers


class PlaylistSerializers(serializers.ModelSerializer):
    music_list = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = [
            "id",
            "title",
            "heart",
            "description",
            "number_of_music",
            "image",
            "author_name",
            "music_list",
        ]

    def get_music_list(self, obj):
        serializer = MusicSerializers(obj.musics, many=True)
        return serializer.data

    def get_author_name(self, obj):
        return obj.author.name


class PlaylistLimitMusicSerializers(serializers.ModelSerializer):
    music_list = MusicSerializers(many=True)

    class Meta:
        model = Playlist
        fields = ["id", "title", "heart", "number_of_music", "image", "music_list"]


class PlaylistAddSerializers(serializers.Serializer):
    music_id = serializers.IntegerField(required=True)


class PlaylistUpdateSerializers(serializers.Serializer):
    title = serializers.CharField()
    image = serializers.ImageField()
    description = serializers.CharField()
