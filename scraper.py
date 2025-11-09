import time
import requests
import schedule
from bs4 import BeautifulSoup

def get_book_data(book_url: str) -> dict:
    """
    Получает данные о книге со страницы сайта

    Args:
        book_url (str): URL страницы книги.

    Returns:
        dict: Словарь с данными о книге (название, цена, рейтинг и т.д.).
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    response = requests.get(book_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('div', class_='product_main').find('h1').text.strip()
    price = soup.find('p', class_='price_color').text.strip().replace('Â', '')
    rating_tag = soup.find('p', class_='star-rating')
    rating = rating_tag['class'][1] if rating_tag else None
    availability = soup.find('p', class_='instock availability').text.strip()

    description_tag = soup.find('div', id='product_description')
    description = (
        description_tag.find_next_sibling('p').text.strip()
        if description_tag else None
    )

    book_data = {
        'title': title,
        'price': price,
        'rating': rating,
        'availability': availability,
        'description': description,
    }

    table = soup.find('table', class_='table table-striped')
    if table:
        for row in table.find_all('tr'):
            key = row.find('th').text.strip()
            value = row.find('td').text.strip()
            if key.lower() not in [k.lower() for k in book_data.keys()]:
                book_data[key] = value

    return book_data

def scrape_books(is_save: bool = False) -> list:
    """
    Собирает данные о всех книгах в каталоге с сайта Books to Scrape.

    Args:
        save_to_file (bool): Если True, сохраняет результат в файл
            books_data.txt в текущей папке. По умолчанию параметр имеет значения False.

    Returns:
        list: Список словарей с данными о книгах.
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
    all_books = []
    page_number = 1

    while True:
        page_url = base_url.format(page_number)
        response = requests.get(page_url)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        book_links = soup.select('h3 a')

        if not book_links:
            break

        for link in book_links:
            relative_url = link['href']
            full_url = (
                'http://books.toscrape.com/catalogue/' +
                relative_url.replace('../../../', '')
            )

            try:
                book_data = get_book_data(full_url)
                all_books.append(book_data)
            except Exception:
                continue

        page_number += 1

    if is_save:
        with open('books_data.txt', 'w', encoding='utf-8') as file:
            for book in all_books:
                file.write(str(book) + '\n')

    return all_books

def task():
    """
    Функция для автоматического запуска функции сбора данных о книгах каждый день
    в 19:00 и сохранение данных в файл.
    """

    print("Запуск сбора данных о книгах...")
    scrape_books(is_save=True)
    print("Сбор данных завершен.")

schedule.every().day.at("19:00").do(task)

while True:
    schedule.run_pending()
    time.sleep(60)