from rest_framework import serializers
from music.models import Artist


class ArtistSerializers(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = "__all__"
        ordering = ["create_at"]
