import pytest
from unittest.mock import Mock, patch
from burger import Burger
from bun import Bun
from ingredient import Ingredient
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestBurger:
    """Тесты для класса Burger"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.burger = Burger()

    def test_burger_initialization(self):
        """Тест инициализации бургера"""
        assert self.burger.bun is None
        assert self.burger.ingredients == []

    def test_set_buns(self):
        """Тест установки булочек"""
        mock_bun = Mock(spec=Bun)
        self.burger.set_buns(mock_bun)
        assert self.burger.bun == mock_bun

    @pytest.mark.parametrize("ingredient_type, name, price", [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_FILLING, "cutlet", 200),
        (INGREDIENT_TYPE_SAUCE, "sour cream", 150)
    ])
    def test_add_ingredient(self, ingredient_type, name, price):
        """Тест добавления ингредиентов"""
        ingredient = Ingredient(ingredient_type, name, price)
        self.burger.add_ingredient(ingredient)
        assert len(self.burger.ingredients) == 1
        assert self.burger.ingredients[0] == ingredient

    def test_add_multiple_ingredients(self):
        """Тест добавления нескольких ингредиентов"""
        ingredient1 = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        ingredient2 = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 200)
        
        self.burger.add_ingredient(ingredient1)
        self.burger.add_ingredient(ingredient2)
        
        assert len(self.burger.ingredients) == 2
        assert self.burger.ingredients[0] == ingredient1
        assert self.burger.ingredients[1] == ingredient2

    def test_remove_ingredient(self):
        """Тест удаления ингредиента"""
        ingredient1 = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        ingredient2 = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 200)
        
        self.burger.add_ingredient(ingredient1)
        self.burger.add_ingredient(ingredient2)
        
        self.burger.remove_ingredient(0)
        assert len(self.burger.ingredients) == 1
        assert self.burger.ingredients[0] == ingredient2

    def test_move_ingredient(self):
        """Тест перемещения ингредиента"""
        ingredient1 = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        ingredient2 = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 200)
        ingredient3 = Ingredient(INGREDIENT_TYPE_SAUCE, "sour cream", 150)
        
        self.burger.add_ingredient(ingredient1)
        self.burger.add_ingredient(ingredient2)
        self.burger.add_ingredient(ingredient3)
        
        # Перемещаем первый ингредиент в конец
        self.burger.move_ingredient(0, 2)
        
        assert self.burger.ingredients[0] == ingredient2
        assert self.burger.ingredients[1] == ingredient3
        assert self.burger.ingredients[2] == ingredient1

    @pytest.mark.parametrize("bun_price, ingredient_prices, expected_total", [
        (100, [50, 75], 325),  # 100*2 + 50 + 75 = 325
        (200, [100, 150, 200], 850),  # 200*2 + 100 + 150 + 200 = 850
        (50, [], 100),  # 50*2 + 0 = 100
        (0, [25, 30], 55),  # 0*2 + 25 + 30 = 55
    ])
    def test_get_price(self, bun_price, ingredient_prices, expected_total):
        """Тест расчета цены бургера с параметризацией"""
        # Создаем мок булочки
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        
        self.burger.set_buns(mock_bun)
        
        # Добавляем ингредиенты с моками
        for price in ingredient_prices:
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = price
            self.burger.add_ingredient(mock_ingredient)
        
        total_price = self.burger.get_price()
        assert total_price == expected_total

    def test_get_price_without_bun(self):
        """Тест расчета цены без булочки"""
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        self.burger.add_ingredient(ingredient)
        
        # Без булочки должен быть AttributeError
        with pytest.raises(AttributeError):
            self.burger.get_price()

    @patch('burger.Burger.get_price')
    def test_get_receipt(self, mock_get_price):
        """Тест генерации чека с моком"""
        mock_get_price.return_value = 350
        
        # Создаем мок булочки
        mock_bun = Mock()
        mock_bun.get_name.return_value = "black bun"
        
        self.burger.set_buns(mock_bun)
        
        # Добавляем ингредиенты
        ingredient1 = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        ingredient2 = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 200)
        self.burger.add_ingredient(ingredient1)
        self.burger.add_ingredient(ingredient2)
        
        receipt = self.burger.get_receipt()
        
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

    def test_get_receipt_empty_burger(self):
        """Тест генерации чека для пустого бургера"""
        mock_bun = Mock()
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 0
        
        self.burger.set_buns(mock_bun)
        
        receipt = self.burger.get_receipt()
        
        expected_lines = [
            "(==== white bun ====)",
            "(==== white bun ====)",
            "",
            "Price: 0"
        ]
        expected_receipt = "\n".join(expected_lines)
        
        assert receipt == expected_receipt

    def test_get_receipt_without_bun(self):
        """Тест генерации чека без булочки"""
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        self.burger.add_ingredient(ingredient)
        
        # Без булочки должен быть AttributeError
        with pytest.raises(AttributeError):
            self.burger.get_receipt()
