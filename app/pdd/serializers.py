from rest_framework import serializers

from core.models import VideoObj, Pdd


class VideoObjSerializer(serializers.ModelSerializer):
    """Serializer for video object"""

    class Meta:
        model = VideoObj
        fields = ('id', 'title')
        read_only_Fields = ('id',)


class PddSerializer(serializers.ModelSerializer):
    """Serialize a PDD object"""

    videos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=VideoObj.objects.all()
    )

    class Meta:
        model = Pdd
        fields = (
            'id', 'videos', 'timestamp', 'name',
        )
        read_only_fields = ('id',)


class PddDetailSerializer(PddSerializer):
    videos = VideoObjSerializer(many=True, read_only=True)
