import pytest
from unittest.mock import Mock, patch
from burger import Burger
from bun import Bun
from ingredient import Ingredient
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestBurger:
    """Тесты для класса Burger"""


    def test_burger_initialization(self, burger):
        """Тест инициализации бургера"""
        assert burger.bun is None
        assert burger.ingredients == []

    def test_set_buns(self, burger):
        """Тест установки булочек"""
        mock_bun = Mock(spec=Bun)
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    @pytest.mark.parametrize("ingredient_type, name, price", [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_FILLING, "cutlet", 200),
        (INGREDIENT_TYPE_SAUCE, "sour cream", 150)
    ])
    def test_add_ingredient(self, burger, ingredient_type, name, price):
        """Тест добавления ингредиентов"""
        ingredient = Ingredient(ingredient_type, name, price)
        burger.add_ingredient(ingredient)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ingredient

    def test_add_multiple_ingredients(self, burger):
        """Тест добавления нескольких ингредиентов"""
        ingredient1 = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        ingredient2 = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 200)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] == ingredient1
        assert burger.ingredients[1] == ingredient2

    def test_remove_ingredient(self, burger):
        """Тест удаления ингредиента"""
        ingredient1 = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        ingredient2 = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 200)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ingredient2

    def test_move_ingredient(self, burger):
        """Тест перемещения ингредиента"""
        ingredient1 = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        ingredient2 = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 200)
        ingredient3 = Ingredient(INGREDIENT_TYPE_SAUCE, "sour cream", 150)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.add_ingredient(ingredient3)
        
        # Перемещаем первый ингредиент в конец
        burger.move_ingredient(0, 2)
        
        assert burger.ingredients[0] == ingredient2
        assert burger.ingredients[1] == ingredient3
        assert burger.ingredients[2] == ingredient1

    @pytest.mark.parametrize("bun_price, ingredient_prices, expected_total", [
        (100, [50, 75], 325),  # 100*2 + 50 + 75 = 325
        (200, [100, 150, 200], 850),  # 200*2 + 100 + 150 + 200 = 850
        (50, [], 100),  # 50*2 + 0 = 100
        (0, [25, 30], 55),  # 0*2 + 25 + 30 = 55
    ])
    def test_get_price(self, burger, bun_price, ingredient_prices, expected_total):
        """Тест расчета цены бургера с параметризацией"""
        # Создаем мок булочки
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        
        burger.set_buns(mock_bun)
        
        # Добавляем ингредиенты с моками
        for price in ingredient_prices:
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)
        
        total_price = burger.get_price()
        assert total_price == expected_total

    def test_get_price_without_bun(self, burger):
        """Тест расчета цены без булочки"""
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        burger.add_ingredient(ingredient)
        
        # Без булочки должен быть AttributeError
        with pytest.raises(AttributeError):
            burger.get_price()

    @patch('burger.Burger.get_price')
    def test_get_receipt(self, mock_get_price, burger):
        """Тест генерации чека с моком"""
        mock_get_price.return_value = 350
        
        # Создаем мок булочки
        mock_bun = Mock()
        mock_bun.get_name.return_value = "black bun"
        
        burger.set_buns(mock_bun)
        
        # Добавляем ингредиенты
        ingredient1 = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        ingredient2 = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 200)
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        receipt = burger.get_receipt()
        
        expected_lines = [
            "(==== black bun ====)",
            "= sauce hot sauce =",
            "= filling cutlet =",
            "(==== black bun ====)",
            "",
            "Price: 350"
        ]
        expected_receipt = "\n".join(expected_lines)
        
        assert receipt == expected_receipt

    def test_get_receipt_empty_burger(self, burger):
        """Тест генерации чека для пустого бургера"""
        mock_bun = Mock()
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 0
        
        burger.set_buns(mock_bun)
        
        receipt = burger.get_receipt()
        
        expected_lines = [
            "(==== white bun ====)",
            "(==== white bun ====)",
            "",
            "Price: 0"
        ]
        expected_receipt = "\n".join(expected_lines)
        
        assert receipt == expected_receipt

    def test_get_receipt_without_bun(self, burger):
        """Тест генерации чека без булочки"""
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        burger.add_ingredient(ingredient)
        
        # Без булочки должен быть AttributeError
        with pytest.raises(AttributeError):
            burger.get_receipt()
