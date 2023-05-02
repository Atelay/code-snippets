import os
import json
from time import sleep, time
from re import sub, search

import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


PARSING_DIR = os.path.abspath(os.path.dirname(__name__))

URL = "https://spb.zoon.ru/medical/?search_query_form=1&m%5B5200e522a0f302f066000055%5D=1&center%5B%5D=59.91878264665887&center%5B%5D=30.342586983263384&zoom=10"
DRIVER = os.path.join(PARSING_DIR, "chromedriver", "chromedriver.exe")
PATH_TO_HTML = os.path.join(PARSING_DIR,"output_data", "page.html")
PATH_TO_TXT = os.path.join(PARSING_DIR,"output_data", "list_of companies_URL.txt")
HEADERS = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64"
}


def get_source_html(url):
    # Подавление раздражающих ошибок Селениума в консоли. Работает на Винде
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # Инициализация драйвера по указаному пути и открытие браузера
    driver = webdriver.Chrome(service=Service(DRIVER), options=options)
    driver.maximize_window() # Полноекранный режим
    try:
        driver.get(url)
        sleep(3) # Это ожидание нужно для полноценной загрузки страницы
        print('[+] Start pages parsing')
        while True:
            sleep(3) # Это ожидание нужно для прогрузки кнопки следующего елемента после прокрутки
            if driver.find_elements(By.CLASS_NAME, "hasmore-text"):
                print('[+] Finish parsing pages')
                os.makedirs("output_data", exist_ok=True)
                with open(os.path.join("output_data", "page.html"), 'w', encoding="utf-8") as file:
                    file.write(driver.page_source)
                print('[+] The page was saved in "output_data" directory in "page.html" file.')
                break  # Если на странице есть элемент "hasmore-text", то выходим из цикла
            else:
                find_more_element = driver.find_element(By.CLASS_NAME, "catalog-button-showMore")  # Ищем кнопку для загрузки дополнительных результатов
                # С помощью ActionChains прокручиваем страницу до кнопки и кликаем на нее
                actions = ActionChains(driver)
                actions.move_to_element(find_more_element).perform()  # С помощью ActionChains прокручиваем страницу до кнопки и кликаем на нее
                find_more_element.click()
    except Exception as ex:
        print(ex)
    finally:
        driver.close()  # Закрытие текущего активного окна браузера
        driver.quit()  # Закрытие всех окон браузера и завершение процесса драйвера.



def get_links_to_company(file_path):
    with open(file_path, encoding="UTF-8") as file:
        src = file.read()
    os.remove(file_path)
    soup = bs(src, "lxml")
    all_minicard_blocks = soup.find_all("div", class_="minicard-item__info") #ищем инфо-блоки поликлиник
    list_of_links = []
    for minicard in all_minicard_blocks:
        link = minicard.find("h2", class_="minicard-item__title").find("a").get("href") # Вытягиваем ссылки
        list_of_links.append(link) 
    os.makedirs("output_data", exist_ok=True)
    with open(os.path.join("output_data", "list_of companies_URL.txt"), "w", encoding="UTF-8") as file:
        for url in list_of_links:
            file.write(f"{url}\n")
    print("[+] URL list of companies is received")


def get_all_data(file_path):
    with open(file_path, encoding="UTF-8") as file:
        url_list = [url.strip() for url in file.readlines()]
    os.remove(file_path)
    result_json_file = []
    count = 1
    list_links_len = len(url_list)
    for url in url_list: # Проходим по ссылкам из файла
        response = requests.get(url=url, headers=HEADERS)
        soup = bs(response.text, 'lxml')

        try:
            # Получение названия компании
            company_name = soup.find('span', {"itemprop": "name"}).text.strip()
        except:
            company_name = None

        try:
            # Получение списка телефонных номеров компании
            find_phones = soup.find('div', class_="service-phones-list").find_all("a", class_="js-phone-number")
            company_phones = [phone.get('href').split(":")[-1].strip() for phone in find_phones]
        except:
            company_phones = None

        try:
            # Получение адреса компании
            company_address = soup.find('address', class_="iblock").text.strip()
            if search(r"\s{2,}", company_address):  # Проверка на наличие более одного пробела между словами
                company_address = sub(r"\s{2,}", " ", company_address)  # Удаление, если таковы имеются
        except:
            company_address = None

        try:
            # Получение ссылки на веб-сайт компании
            company_website = soup.find('div', class_="service-website-value").find('a').text.strip()
        except:
            company_website = None

        try:
            # Получение списка ссылок на соцсети компании
            social_networks = soup.find('div', class_="js-service-socials").find_all('a')
            company_social_links = [unquote(social.get('href').split("?to=")[1].split("&")[0]) for social in social_networks]
        except:
            company_social_links = None
        result_json_file.append(
            {
                "company_name": company_name,
                "Link": url,
                "Phone_number": company_phones,
                "Address": company_address,
                "Website": company_website,
                "Social_networks": company_social_links,
            }
        )
        progress = count / list_links_len  # Делим текущее значение счетчика на общее число ссылок
        filled_length = int(50 * progress)  # Вычисляем длину заполненной части шкалы. 50-общее число символов в строке прогресса
        bar = '█' * filled_length + '-' * (50 - filled_length)  # Создаем строку прогресса, состоящую из символов.
        print(f"\r[+] Processed: {count}/{list_links_len} |{bar}| {progress:.2%}", end="", flush=True)  # Устанавливаем каретку вначале строки чтобы не перезаписывать каждый раз. :.2% - 2 знака после запятой и вывод в процентном виде.
        count += 1
    os.makedirs("output_data", exist_ok=True)
    with open(os.path.join("output_data",'result.json'), 'w', encoding='UTF-8') as file:
        json.dump(result_json_file, file, indent=4, ensure_ascii=False)
    print("\n[+] The data was saved in JSON file.")


def main():
    get_source_html(URL)
    # get_links_to_company(PATH_TO_HTML)
    # get_all_data(PATH_TO_TXT)

if __name__ == "__main__":
    y = time()
    main()
    x = time()
    print(f"Time spent: {round(x-y, 2)} seconds")


