from rest_framework import viewsets, mixins
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
