from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import (RefreshToken)

from users.models import User
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient


class RecipesTests(APITestCase):
    """
    Тестирование доступности эндпоинтов приложения recipes.
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
        self.recipe = Recipe.objects.create(
            name='Варенный картофель',
            text='Зачем нужно есть капусту когда есть картошка',
            cooking_time='10',
            author=self.user,
        )
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            amount='10'
        )
        self.recipe.tags.add(self.tag.pk)
        self.anon_client = APIClient()
        token = RefreshToken.for_user(self.user)
        self.token = str(token.access_token)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_tag_get_requests(self):
        pk = self.tag.pk
        url = reverse('api:tags-list')
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api:tags-detail', kwargs={'pk': pk})
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ingredients_get_requests(self):
        pk = self.ingredient.pk
        url = reverse('api:ingredients-list')
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api:ingredients-detail', kwargs={'pk': pk})
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recipe_get_requests(self):
        pk = self.recipe.pk
        url = reverse('api:recipes-list')
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api:recipes-detail', kwargs={'pk': pk})
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    def test_recipe_post_requests(self):
        url = reverse('api:recipes-list')
        pk_ingredient = self.ingredient.pk
        pk_tag = self.tag.pk
        data = {
            "ingredients": [{"id": pk_ingredient, "amount": 1}],
            "tags": [pk_tag],
            "image": (
                "data:image/png;base64,iV"
                "BORw0KGgoAAAANSUhEUgAAAAE"
                "AAAABAgMAAABieywaAAAACVBMV"
                "EUAAAD///9fX1/S0ecCAAAACXBI"
                "WXMAAA7EAAAOxAGVKw4bAAAACkl"
                "EQVQImWNoAAAAggCByxOyYQAAAAB"
                "JRU5ErkJggg=="
                ),
            "name": "Риба на пару",
            "text": "Пар",
            "coocing_time": 10
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.anon_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    """

    def test_recipe_patch_requests(self):
        pk = self.recipe.pk
        pk_ingredient = self.ingredient.pk
        pk_tag = self.tag.pk
        url = reverse('api:recipes-detail', kwargs={'pk': pk})
        data = {
            "ingredients": [{"id": pk_ingredient, "amount": 1}],
            "tags": [pk_tag],
            "image": (
                "data:image/png;base64,iV"
                "BORw0KGgoAAAANSUhEUgAAAAE"
                "AAAABAgMAAABieywaAAAACVBMV"
                "EUAAAD///9fX1/S0ecCAAAACXBI"
                "WXMAAA7EAAAOxAGVKw4bAAAACkl"
                "EQVQImWNoAAAAggCByxOyYQAAAAB"
                "JRU5ErkJggg=="
                ),
            "name": "Риба на пару",
            "text": "Пар",
            "coocing_time": 10
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.anon_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_recipe_delete_requests(self):
        pk = self.recipe.pk
        url = reverse('api:recipes-detail', kwargs={'pk': pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.anon_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_favorite(self):
        pk = self.recipe.pk
        url = reverse('api:recipes-detail', kwargs={'pk': pk})
        url = f'{url}favorite/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.anon_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)