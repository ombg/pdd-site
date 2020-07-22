from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import VideoObj, Pdd

from pdd import serializers


class VideoObjViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin):
    """Manage videos in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = VideoObj.objects.all()
    serializer_class = serializers.VideoObjSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-title')

    def perform_create(self, serializer):
        """
        Create a new video object
        by overriding CreateModelMixin::perform_create()
        """
        serializer.save(user=self.request.user)


class PddViewSet(viewsets.ModelViewSet):
    """Manage PDD objects in the database"""
    serializer_class = serializers.PddSerializer
    queryset = Pdd.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the PDD objects for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.PddDetailSerializer
        elif self.action == 'upload_video':
            return serializers.PddVideoSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new PDD object"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-video')
    def upload_video(self, request, pk=None):
        """Upload a video to a PDD object."""
        pddobj = self.get_object()
        serializer = self.get_serializer(
            pddobj,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,  # id plus video
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
