import pytest
from unittest.mock import patch, Mock
from database import Database
from bun import Bun
from ingredient import Ingredient
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestDatabase:
    """Тесты для класса Database"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.database = Database()

    def test_database_initialization(self):
        """Тест инициализации базы данных"""
        assert len(self.database.buns) == 3
        assert len(self.database.ingredients) == 6

    def test_available_buns(self):
        """Тест метода available_buns"""
        buns = self.database.available_buns()
        assert len(buns) == 3
        assert all(isinstance(bun, Bun) for bun in buns)

    def test_available_ingredients(self):
        """Тест метода available_ingredients"""
        ingredients = self.database.available_ingredients()
        assert len(ingredients) == 6
        assert all(isinstance(ingredient, Ingredient) for ingredient in ingredients)

    @pytest.mark.parametrize("expected_bun_name, expected_bun_price", [
        ("black bun", 100),
        ("white bun", 200),
        ("red bun", 300)
    ])
    def test_buns_data(self, expected_bun_name, expected_bun_price):
        """Тест данных булочек с параметризацией"""
        buns = self.database.available_buns()
        bun_names = [bun.get_name() for bun in buns]
        bun_prices = [bun.get_price() for bun in buns]
        
        assert expected_bun_name in bun_names
        assert expected_bun_price in bun_prices

    @pytest.mark.parametrize("expected_ingredient_name, expected_ingredient_type, expected_ingredient_price", [
        ("hot sauce", INGREDIENT_TYPE_SAUCE, 100),
        ("sour cream", INGREDIENT_TYPE_SAUCE, 200),
        ("chili sauce", INGREDIENT_TYPE_SAUCE, 300),
        ("cutlet", INGREDIENT_TYPE_FILLING, 100),
        ("dinosaur", INGREDIENT_TYPE_FILLING, 200),
        ("sausage", INGREDIENT_TYPE_FILLING, 300)
    ])
    def test_ingredients_data(self, expected_ingredient_name, expected_ingredient_type, expected_ingredient_price):
        """Тест данных ингредиентов с параметризацией"""
        ingredients = self.database.available_ingredients()
        ingredient_names = [ingredient.get_name() for ingredient in ingredients]
        ingredient_types = [ingredient.get_type() for ingredient in ingredients]
        ingredient_prices = [ingredient.get_price() for ingredient in ingredients]
        
        assert expected_ingredient_name in ingredient_names
        assert expected_ingredient_type in ingredient_types
        assert expected_ingredient_price in ingredient_prices

    def test_buns_structure(self):
        """Тест структуры булочек"""
        buns = self.database.available_buns()
        
        # Проверяем, что все булочки имеют правильную структуру
        for bun in buns:
            assert hasattr(bun, 'name')
            assert hasattr(bun, 'price')
            assert hasattr(bun, 'get_name')
            assert hasattr(bun, 'get_price')
            assert callable(bun.get_name)
            assert callable(bun.get_price)

    def test_ingredients_structure(self):
        """Тест структуры ингредиентов"""
        ingredients = self.database.available_ingredients()
        
        # Проверяем, что все ингредиенты имеют правильную структуру
        for ingredient in ingredients:
            assert hasattr(ingredient, 'type')
            assert hasattr(ingredient, 'name')
            assert hasattr(ingredient, 'price')
            assert hasattr(ingredient, 'get_type')
            assert hasattr(ingredient, 'get_name')
            assert hasattr(ingredient, 'get_price')
            assert callable(ingredient.get_type)
            assert callable(ingredient.get_name)
            assert callable(ingredient.get_price)

    def test_sauce_ingredients_count(self):
        """Тест количества соусов"""
        ingredients = self.database.available_ingredients()
        sauce_count = sum(1 for ingredient in ingredients if ingredient.get_type() == INGREDIENT_TYPE_SAUCE)
        assert sauce_count == 3

    def test_filling_ingredients_count(self):
        """Тест количества начинок"""
        ingredients = self.database.available_ingredients()
        filling_count = sum(1 for ingredient in ingredients if ingredient.get_type() == INGREDIENT_TYPE_FILLING)
        assert filling_count == 3

    def test_unique_bun_names(self):
        """Тест уникальности названий булочек"""
        buns = self.database.available_buns()
        bun_names = [bun.get_name() for bun in buns]
        assert len(bun_names) == len(set(bun_names))

    def test_unique_ingredient_names(self):
        """Тест уникальности названий ингредиентов"""
        ingredients = self.database.available_ingredients()
        ingredient_names = [ingredient.get_name() for ingredient in ingredients]
        assert len(ingredient_names) == len(set(ingredient_names))
