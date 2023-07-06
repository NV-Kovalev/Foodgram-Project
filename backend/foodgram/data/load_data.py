import csv

from recipes.models import Ingredient
from foodgram.settings import data_path


def fill_ingredients_from_csv():
    """Функция для заполнения модели Ingredients из csv файла."""
    with open(data_path, 'r') as file:
        reader = csv.reader(file)
        for obj in reader:
            ingredient = Ingredient(name=obj[0], measurement_unit=obj[1])
            ingredient.save()
