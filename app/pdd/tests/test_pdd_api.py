from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Pdd

from pdd.serializers import PddSerializer


PDD_URL = reverse('pdd:pdd-list')


def sample_pdd_obj(user, **params):
    """Create and return a sample pdd object"""
    defaults = {
        'name': 'Sample PDD object',
        'timestamp': '2000-01-01 08:00:00-07:00',
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
