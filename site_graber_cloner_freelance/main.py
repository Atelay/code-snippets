from bs4 import BeautifulSoup as bs
import aiohttp
import asyncio
import json
from time import time
import os


DIR_NAME = "result"
FILE_NAME = "News"
WEBSITE = "https://hi-tech.ua/news/"
PARSING_DIR = os.path.abspath(os.path.dirname(__name__))
HEADERS = {
    "accept": "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64"
}


async def get_articles_urls(url):
    async with aiohttp.ClientSession() as session:
        articles_response = await session.get(url=url, headers=HEADERS, ssl=False, timeout=aiohttp.ClientTimeout(total=None))
        articles_soup = bs(await articles_response.text(), "lxml")
        total_page_count = articles_soup.find("div", class_="pagination").find_all("a")[-1].get("href").strip("/").split("/")[-1]
        fetch_page_tasks = [_get_page(session, i) for i in range(1, int(250)+1)]
        articles_page_results = await asyncio.gather(*fetch_page_tasks)
        articles_urls_list = [item for sublist in articles_page_results for item in sublist]
        os.makedirs(DIR_NAME, exist_ok=True)
        with open(os.path.join(PARSING_DIR, DIR_NAME, f'{FILE_NAME}.txt'), 'w', encoding='UTF-8') as file:
            [file.write(f"{url}\n") for url in articles_urls_list]


async def _get_page(session: aiohttp.ClientSession, page: int):
    page_url = f"{WEBSITE}page/{page}/"
    async with session.get(page_url, headers=HEADERS, ssl=False, timeout=aiohttp.ClientTimeout(total=None)) as response:
        soup = bs(await response.text(), 'lxml')
    results = soup.find_all('div', {'class': 'single-post-news-page'})
    return [result.find('a').get('href').strip() for result in results]


async def get_post_dates(urls_file_path: str):
    with open(urls_file_path, encoding="UTF-8") as file:
        list_of_url = [url.strip() for url in file.readlines()]
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = []

        for url in list_of_url:
            tasks.append(asyncio.ensure_future(parse_post_data(session, url)))
        post_dates = await asyncio.gather(*tasks)
        with open(os.path.join(PARSING_DIR, DIR_NAME, f'{FILE_NAME}.json'), 'w', encoding='UTF-8') as file:
            json.dump(post_dates, file, indent=4, ensure_ascii=False)
        print(f'{len(list_of_url)} articles were received. They were saved in the current directory, in the `result` folder, in the `News.json` file.')


async def parse_post_data(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = bs(html, 'html.parser')
        post_title = soup.find('div', class_='main-content-single').find('h1').text
        post_date = soup.find('span', class_='single-post-date').text.strip()
        post_photo_url = list(set(img['src'] for p in soup.find_all('p') for img in p.find_all('img', class_='alignnone') if not img['src'].endswith(".gif")))
        post_plain_text = [i.text.strip() for i in soup.find_all('p')]
        formatted_post_text = "".join(post_plain_text[:post_plain_text.index("Ваша email адреса не буде опублікована. Обов'язкові поля позначені *")])
        return {
            "original_url": url,
            "post_title":post_title,
            "post_date": post_date,
            "photo_url": post_photo_url,
            "post_text": formatted_post_text,
        }


def main():
    asyncio.run(get_articles_urls(url=WEBSITE))
    asyncio.run(get_post_dates(os.path.join(PARSING_DIR, DIR_NAME, f'{FILE_NAME}.txt')))


if __name__ == "__main__":
    start = time()
    main()
    finish = time()
    x = divmod(round(finish-start),60)
    print(f"Time spent: {x[0]} minutes {x[1]} seconds")
