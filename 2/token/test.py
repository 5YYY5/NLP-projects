# Импортируем модули:
# requests - для отправки запроса и получения
# HTML-содержимого данной веб-страницы.
# BeautifulSoup - для извлечения информации с
# веб-страниц и использовать ее для различных
# целей, таких как парсинг новостей, получение
# данных с целевых сайтов, анализ HTML-кода...
import requests
from bs4 import BeautifulSoup
# Зададим адрес веб-страницы, с которой будем брать информацию.
# В данном случае это страница поиска команды для скачивания
# пакета requests с помощью conda
url = "https://anaconda.org/conda-forge/requests/"
# url = " "
# Отправим запрос и проверим, что страницу удалось загрузить
success_code = 200 # Прописан в самой библиотеке
# try-except-блок служит для обработки исключений
try:
    r = requests.get(url)
except:
    print("Bad url. Exiting program...")
    exit()
if r.status_code != success_code:
    # Если загрузка не удалась выведется сообщение об ошибке
    # и программа завершит свою работу
    print("Failed to load web page {}".format(url))
    exit()
show_content = True
# Можно напечатать и посмотреть, в каком виде мы получает страницу:
# для этого надо флаг show_content установить в True
if show_content:
    print("Web page after request:\n{}".format(r.content))
# Чтобы привести страницу к более наглядному виду преобразуем ее кодировку
# с помощью BeautifulSoup
soup = BeautifulSoup(r.content, 'html.parser')
if show_content:
    print("Prettier view:\n{}".format(soup.prettify()))
# Мы хотим всегда брать первую команду из предложенных
# (как обычно в программировании считаем с 0)
num_of_command = 0
# Если открыть страницу в режиме инспектирования, то можно
# видеть, что все команды имеют тег <code>
# Отлично! Значит осталось собрать все места с code и выбрать
# нужную строку.
soupTags = soup.find_all('code')
# Метод text очистит строку от тегов и вернет просто текст
if soupTags:
    print(soupTags[num_of_command].text)
else:
    print("No command found.")