from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import VideoObj

from pdd.serializers import VideoObjSerializer


VIDEOS_URL = reverse('pdd:videoobj-list')


class PublicVideoObjApiTests(TestCase):
    """Test the publicly available video obj API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving videos"""
        res = self.client.get(VIDEOS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateVideoObjApiTests(TestCase):
    """Test the authorized user video API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_videos(self):
        """Test retrieving videos"""
        VideoObj.objects.create(user=self.user, title='Jurassic Park')
        VideoObj.objects.create(user=self.user, title='back to the Future')

        res = self.client.get(VIDEOS_URL)

        videos = VideoObj.objects.all().order_by('-title')
        serializer = VideoObjSerializer(videos, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_videos_limited_to_user(self):
        """Test that videos returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'testpass'
        )
        VideoObj.objects.create(user=user2, title='Jurassic Park')
        video = VideoObj.objects.create(
            user=self.user,
            title='back to the future III'
        )

        res = self.client.get(VIDEOS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], video.title)

    def test_create_videoobj_successful(self):
        """Test creating a new video object"""
        payload = {'title': 'Simple'}
        self.client.post(VIDEOS_URL, payload)

        exists = VideoObj.objects.filter(
            user=self.user,
            title=payload['title']
        ).exists()
        self.assertTrue(exists)

    def test_create_videoobj_invalid(self):
        """Test creating a new video object with invalid payload"""
        payload1 = {'name': 'Hello again'}
        payload2 = {'title': ''}
        res = self.client.post(VIDEOS_URL, payload1)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        res = self.client.post(VIDEOS_URL, payload2)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
