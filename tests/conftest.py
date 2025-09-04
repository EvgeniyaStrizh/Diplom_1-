import pytest
from burger import Burger
from database import Database


@pytest.fixture
def burger():
    """Фикстура для создания экземпляра Burger"""
    return Burger()


@pytest.fixture
def database():
    """Фикстура для создания экземпляра Database"""
    return Database()
