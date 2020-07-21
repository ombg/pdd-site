from rest_framework import serializers

from core.models import VideoObj


class VideoObjSerializer(serializers.ModelSerializer):
    """Serializer for video object"""

    class Meta:
        model = VideoObj
        fields = ('id', 'title')
        read_only_Fields = ('id',)
