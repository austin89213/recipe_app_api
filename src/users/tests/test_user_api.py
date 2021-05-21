from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """ Test the users API (public) """
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """  Test creating user with valid payload is successful """
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        print(user.password)
        password_check = False
        if user.password == payload['password']:
            password_check = True
        self.assertTrue(password_check)
        self.assertNotIn('password', res.data)

    def tset_user_exits(self):
        """  Test creating user that already exists fails """
        payload = {'email': 'test@gamil.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """" Test that password must be more than 5 characters """
        payload = {'email': 'test@gamil.com', 'password': 'test'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """  Test that a token is created for the user """
        payload = {'email': 'test@gmail.com.tw', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('toekn', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@londonappdev.com', password='testpass')
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """  Test that token is not created if user doesn't exist """
        payload = {'email': 'test@gmail.com.tw', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ "Test that email and password are required """
        res = self.client.post(TOKEN_URL, {'email': 'test@gamil.com', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
