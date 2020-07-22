from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


# Helper function
def sample_user(email='test@gmail.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is succesfull"""
        email = 'test@gmail.com'
        password = 'Test1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email for new user is normalized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating new user with an invalid email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'root@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_videoobj_str(self):
        """Test the video object string representation"""
        videoobj = models.VideoObj.objects.create(
            user=sample_user(),
            title='Jurassic Park'
        )

        self.assertEqual(str(videoobj), videoobj.title)

    def test_pddobj_str(self):
        """Test the PDD object string representation"""
        pdd = models.Pdd.objects.create(
            user=sample_user(),
            name='Jurassic Park',
            timestamp='2019-12-25 09:00:00-07:00'
        )

        self.assertEqual(str(pdd), pdd.name)

    @patch('uuid.uuid4')
    def test_pddobj_file_name_uuid(self, mock_uuid):
        """Test that file is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.pddobj_video_file_path(None, 'myvideo.mp4')

        exp_path = f'uploads/videos/{uuid}.mp4'
        self.assertEqual(file_path, exp_path)
