from bs4 import BeautifulSoup
import requests


def weather_check(city):
    """Чтобы узнать Юзер-Агент, нужно на любом зайте открыть меню разработчика, и во вкладке сеть выбрать любой запрос. В самом низу будет эта строка"""
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58"
    }

    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',
        headers=headers
    )

    soup = BeautifulSoup(res.text, 'html.parser')

    time = soup.select('#wob_dts')[0].getText().strip()
    precipitation = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    windy = soup.select("#wob_ws")[0].getText().strip()

    print(f'''Прогноз погоды по состоянию на: {time}
Информация об осадках: {precipitation}
Скорость ветра: {windy}
Температура воздуха: {weather}°C''')


if __name__ == '__main__':
    city_input = input('Введите название города: ')
    weather_check(f'{city_input} погода')
