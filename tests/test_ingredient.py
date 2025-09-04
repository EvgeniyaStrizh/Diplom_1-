import pytest
from ingredient import Ingredient
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestIngredient:
    """Тесты для класса Ingredient"""

    @pytest.mark.parametrize("ingredient_type, name, price", [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_SAUCE, "sour cream", 200),
        (INGREDIENT_TYPE_FILLING, "cutlet", 100),
        (INGREDIENT_TYPE_FILLING, "dinosaur", 200),
        ("", "", 0),
        ("CUSTOM_TYPE", "Very long ingredient name", 999.99)
    ])
    def test_ingredient_initialization(self, ingredient_type, name, price):
        """Тест инициализации ингредиента с различными параметрами"""
        ingredient = Ingredient(ingredient_type, name, price)
        assert ingredient.type == ingredient_type
        assert ingredient.name == name
        assert ingredient.price == price

    @pytest.mark.parametrize("ingredient_type, name, price", [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_SAUCE, "sour cream", 200),
        (INGREDIENT_TYPE_FILLING, "cutlet", 100),
        (INGREDIENT_TYPE_FILLING, "dinosaur", 200)
    ])
    def test_get_type(self, ingredient_type, name, price):
        """Тест метода get_type"""
        ingredient = Ingredient(ingredient_type, name, price)
        assert ingredient.get_type() == ingredient_type

    @pytest.mark.parametrize("ingredient_type, name, price", [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_SAUCE, "sour cream", 200),
        (INGREDIENT_TYPE_FILLING, "cutlet", 100),
        (INGREDIENT_TYPE_FILLING, "dinosaur", 200),
        ("CUSTOM_TYPE", "test ingredient", 0),
        ("ANOTHER_TYPE", "expensive ingredient", 999.99)
    ])
    def test_get_name(self, ingredient_type, name, price):
        """Тест метода get_name"""
        ingredient = Ingredient(ingredient_type, name, price)
        assert ingredient.get_name() == name

    @pytest.mark.parametrize("ingredient_type, name, price", [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_SAUCE, "sour cream", 200),
        (INGREDIENT_TYPE_FILLING, "cutlet", 100),
        (INGREDIENT_TYPE_FILLING, "dinosaur", 200),
        ("CUSTOM_TYPE", "test ingredient", 0),
        ("ANOTHER_TYPE", "expensive ingredient", 999.99)
    ])
    def test_get_price(self, ingredient_type, name, price):
        """Тест метода get_price"""
        ingredient = Ingredient(ingredient_type, name, price)
        assert ingredient.get_price() == price

    def test_ingredient_attributes_access(self):
        """Тест прямого доступа к атрибутам ингредиента"""
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "test sauce", 150)
        assert ingredient.type == INGREDIENT_TYPE_SAUCE
        assert ingredient.name == "test sauce"
        assert ingredient.price == 150
