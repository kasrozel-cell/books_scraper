import pytest
from scraper import get_book_data, scrape_books


def test_get_book_data_returns_dict():
    """
    Проверка, что get_book_data возвращает словарь с нужными ключами.
    """
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    data = get_book_data(url)
    assert isinstance(data, dict)
    expected_keys = ["title", "price", "rating", "availability", "description"]
    for key in expected_keys:
        assert key in data


def test_get_book_data_title_correct():
    """
    Проверка, что название книги корректно.
    """
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    data = get_book_data(url)
    assert data["title"] == "A Light in the Attic"


def test_scrape_books_returns_list():
    """
    Проверка, что scrape_books возвращает список словарей
    и хотя бы одна книга есть на первой странице.
    """
    books = scrape_books(is_save=False)
    assert isinstance(books, list)
    assert len(books) > 0
    assert isinstance(books[0], dict)
    for key in ["title", "price", "rating", "availability", "description"]:
        assert key in books[0]




