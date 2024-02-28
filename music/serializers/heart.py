from rest_framework import serializers
from music.models import Heart


class HeartSerializers(serializers.ModelSerializer):

    class Meta:
        model = Heart
        # fields = "__all__"
        fields = ["user", "music"]
        ordering = ["create_at"]
