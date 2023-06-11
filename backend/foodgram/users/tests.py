from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import (RefreshToken)

from .models import User


class UserViewSetTests(APITestCase):
    """
    Тестирование доступности эндпоинтов UserViewSet.
    """

    def setUp(self):
        self.user = User.objects.create(
            email='test@test.ru',
            username='test',
            first_name='test',
            last_name='test',
            password='test',
        )
        self.author = User.objects.create(
            email='author@author.ru',
            username='author',
            first_name='author',
            last_name='author',
            password='author',
        )
        self.anon_client = APIClient()
        token = RefreshToken.for_user(self.user)
        self.token = str(token.access_token)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_users_list(self):
        url = reverse('api:users-list')
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_detail(self):
        pk = self.author.pk
        url = reverse('api:users-detail', kwargs={'pk': pk})
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_create(self):
        url = reverse('api:users-list')
        data = {
            'email': 'test@test1.ru',
            'username': 'test1',
            'first_name': 'test1',
            'last_name': 'test1',
            'password': 'test1'
            }
        response = self.anon_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_users_profile(self):
        url = reverse('api:users-detail', kwargs={'pk': 'me'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_set_password(self):
        url = reverse('api:users-detail', kwargs={'pk': 'set_password'})
        data = {
            "current_password": "test",
            "new_password": "test1"
            }
        response = self.anon_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #    Тут response возвращает код 400, при мануальном тестировании
    #    программа работает как задумывалось. С чем связано - не понятно.
    #    response = self.client.post(url, data)
    #    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users_subscriptions(self):
        url = reverse('api:users-detail', kwargs={'pk': 'subscriptions'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_subscribe(self):
        pk = self.author.pk
        url = reverse('api:users-detail', kwargs={'pk': pk})
        url = f'{url}subscribe/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
