from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework_simplejwt.tokens import (AccessToken, RefreshToken)

from users.models import User
from recipes.models import Tag, Ingredient


class TagIngredientViewSetTests(APITestCase):
    """
    Тестирование доступности эндпоинтов TagViewSet и IngredientViewSet.
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
        self.tag = Tag.objects.create(
            name='Завтрак',
            slug='breakfast',
            colour='bbe841'
        )
        self.ingredient = Ingredient.objects.create(
            name='Картошка',
            measurement_unit='кг'
        )
        self.anon_client = APIClient()
        token = RefreshToken.for_user(self.user)
        self.token = str(token.access_token)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_tag_list_retrieve(self):
        pk = self.tag.pk
        url = reverse('api:tag-list')
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api:tag-detail', kwargs={'pk': pk})
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ingredients_list_retrieve(self):
        pk = self.ingredient.pk
        url = reverse('api:ingredients-list')
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api:ingredients-detail', kwargs={'pk': pk})
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
