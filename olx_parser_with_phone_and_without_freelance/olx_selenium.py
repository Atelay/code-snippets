from random import choice, randint
import json
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


URLS_PATH = os.path.join("result", "OLX_ads_URLs.txt")
# DRIVER = os.path.join("driver", "chromedriver.exe")
DRIVER = os.path.join("driver", "msedgedriver.exe")

user_agents = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13.3; rv:112.0) Gecko/20100101 Firefox/112.0",
"Mozilla/5.0 (X11; Linux i686; rv:112.0) Gecko/20100101 Firefox/112.0",
"Mozilla/5.0 (X11; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:112.0) Gecko/20100101 Firefox/112.0",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
"Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13.3; rv:102.0) Gecko/20100101 Firefox/102.0",
"Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0",
"Mozilla/5.0 (Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
"Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
]
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")




def get_ads_urls(path):
    with open(path, 'r', encoding='UTF-8') as file:
        return [url.strip() for url in file.readlines()]


def olx_login(driver: webdriver.Edge):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-2gs0sc'))).send_keys(LOGIN)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-ugcges'))).send_keys(PASSWORD)
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-ypypxs"))).click()
    time.sleep(10)




def click_button_on_page(urls, user_agents):

    cookies = None
    options = webdriver.EdgeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-logging'])

    with webdriver.Edge(service=Service(DRIVER), options=options) as driver:
        driver.maximize_window()
        ads_results = []
        count = 0

        for url in urls[:11]:

            if count > 0 and count%5==0:
                print("[+] Sleeping to avoid detection...")
                time.sleep(randint(30, 60))

            # Обновляем юзер-агент и куки перед каждым запросом
            user_agent = choice(user_agents)
            options.add_argument(f'user-agent={user_agent}')
            if cookies != None: 
                for cookie in cookies:
                    driver.add_cookie(cookie)
            driver.get(url)
            time.sleep(randint(10, 30))
            if urls.index(url) == 0: # Логинимся при запуске скрипта
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-cy='dismiss-cookies-overlay']"))).click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-12l1k7f"))).click()
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform() # тест нажатия на ескейп
                olx_login(driver)

            # Получение остальных данных
            try:
                ads_title = driver.find_element(By.TAG_NAME, 'h1').text.strip()
            except Exception:
                ads_title = None
            try:
                ads_price = driver.find_element(By.CSS_SELECTOR, "h3.css-ddweki.er34gjf0").text.strip()
            except Exception:
                ads_price = None
            try:
                ads_date = driver.find_element(By.CSS_SELECTOR, 'span.css-19yf5ek').text.strip()
            except Exception:
                ads_date = None
            try:
                ads_description = driver.find_element(By.CSS_SELECTOR, "div.css-bgzo2k").text.strip()
            except Exception:
                ads_description = None
            try:
                all_photo_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.swiper-slide.css-1915wzc')
                ads_photo_urls = [i.find_element(By.CSS_SELECTOR, "div.swiper-zoom-container img").get_attribute('src').strip()
                                for i in all_photo_blocks]
            except Exception:
                ads_photo_urls = None
            try:
                ads_seller_name = driver.find_element(By.CSS_SELECTOR, 'h4.css-1lcz6o7').text.split()
            except Exception:
                ads_seller_name = None
            # Получение номера телефона с кнопки "Показать" внизу страницы.
            if driver.find_elements(By.XPATH, "//div[@data-testid='phones-container']"):
                try:
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-19zjgsi")))
                    driver.execute_script("window.scrollBy(0, 150);") 
                    ActionChains(driver).click(element).perform()
                    try:
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "css-1478ixo")))
                        find_phone_numbers = (f"{elem.get_attribute('href').split(':')[-1]}" for elem in driver.find_element(By.CLASS_NAME, 'css-1478ixo').find_elements(By.TAG_NAME, "a"))
                        ads_seller_number = [f"{i if i.startswith('+38') else f'+38{i}'}" for i in find_phone_numbers]
                    except Exception:
                        driver.execute_script("window.scrollBy(0, 150);") 
                        ActionChains(driver).click(element).perform()
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "css-1478ixo")))
                        find_phone_numbers = (f"{elem.get_attribute('href').split(':')[-1]}" for elem in driver.find_element(By.CLASS_NAME, 'css-1478ixo').find_elements(By.TAG_NAME, "a"))
                        ads_seller_number = [f"{i if i.startswith('+38') else f'+38{i}'}" for i in find_phone_numbers]
                except Exception:
                    ads_seller_number = None
            else:
                ads_seller_number = None
            # Если нету кнопки Показать, нажать на кнопку "Позвонить"
            if ads_seller_number == None:
                    try:
                        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-1nd8q08")))
                        ActionChains(driver).click(element).perform()
                        try:
                            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@data-testid='primary-phone']")))
                            find_phone_numbers = (f"{elem.get_attribute('href').split(':')[-1]}" for elem in driver.find_element(By.XPATH, "//span[@data-testid='primary-phone']/a"))
                            ads_seller_number = [f"{i if i.startswith('+38') else f'+38{i}'}" for i in find_phone_numbers]
                        except Exception:
                            ActionChains(driver).click(element).perform()
                            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@data-testid='primary-phone']")))
                            find_phone_numbers = (f"{elem.get_attribute('href').split(':')[-1]}" for elem in driver.find_element(By.XPATH, "//span[@data-testid='primary-phone']/a"))
                            ads_seller_number = [f"{i if i.startswith('+38') else f'+38{i}'}" for i in find_phone_numbers]
                            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform() # тест нажатия на ескейп

                    except Exception:
                        ads_seller_number = None
            cookies = driver.get_cookies()
            print(f"[+] Result: {urls.index(url)+1}/{len(urls)}")
            count += 1
            ads_results.append(
                {
                    "ads_url": url,
                    "ads_title": ads_title,
                    "ads_date": ads_date,
                    "ads_price": ads_price,
                    "ads_photos": ads_photo_urls,
                    "ads_description": ads_description,
                    "ads_seller_name": ads_seller_name,
                    "ads_seller_number": ads_seller_number,
                }
            )
        with open(os.path.join("result", "ads_result.json"), 'w', encoding='UTF-8') as file:
            json.dump(ads_results, file, indent=4, ensure_ascii=False)




if __name__ == "__main__":
    x = time.time()
    # print(get_ads_urls(URLS_PATH))
    click_button_on_page(get_ads_urls(URLS_PATH), user_agents)
    y = time.time()
    print(round(y-x, 2))