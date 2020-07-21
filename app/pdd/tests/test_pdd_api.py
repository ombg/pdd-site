
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Pdd, VideoObj

from pdd.serializers import PddSerializer, PddDetailSerializer


PDD_URL = reverse('pdd:pdd-list')


def sample_videoobj(user, title='a video'):
    """Create and return a sample tag"""
    return VideoObj.objects.create(user=user, title=title)


def detail_url(pdd_id):
    """Return PDD obj detail URL"""
    return reverse('pdd:pdd-detail', args=[pdd_id])


def sample_pdd_obj(user, **params):
    """Create and return a sample pdd object"""
    defaults = {
        'name': 'Sample PDD object',
        'timestamp': '2000-01-01T08:00:00-08:00',  # TODO potential bug
    }
    defaults.update(params)
    return Pdd.objects.create(user=user, **defaults)


class PublicPddApiTests(TestCase):
    """Test unauthenticated access to PDD API"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authentication is required"""
        res = self.client.get(PDD_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated pdd API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_pdds(self):
        """Test retrieving list of pdds"""
        sample_pdd_obj(user=self.user)
        sample_pdd_obj(user=self.user)

        res = self.client.get(PDD_URL)

        pdds = Pdd.objects.all().order_by('-id')
        serializer = PddSerializer(pdds, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_pdds_limited_to_user(self):
        """Test retrieving pdds for user"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'pass'
        )
        sample_pdd_obj(user=user2)
        sample_pdd_obj(user=self.user)

        res = self.client.get(PDD_URL)

        pdds = Pdd.objects.filter(user=self.user)
        serializer = PddSerializer(pdds, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_pddobj_detail(self):
        """Test viewing a recipe detail"""
        pdd_obj = sample_pdd_obj(user=self.user)
        pdd_obj.videos.add(sample_videoobj(user=self.user))

        url = detail_url(pdd_obj.id)
        res = self.client.get(url)

        serializer = PddDetailSerializer(pdd_obj)
        self.assertEqual(res.data, serializer.data)