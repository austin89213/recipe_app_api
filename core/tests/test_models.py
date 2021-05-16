from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successfull(self):
        """
        Test creating a new user with am email is successfull
        """
        email = 'test@example.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(
            email=email, password=password, username='austin'
             )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))