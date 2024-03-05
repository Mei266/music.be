from rest_framework import serializers
from music.models import Follow


class FollowSerializers(serializers.ModelSerializer):

    class Meta:
        model = Follow
        # fields = "__all__"
        fields = ["user", "artist"]
        ordering = ["create_at"]
