from bs4 import BeautifulSoup as bs
import lxml
import aiohttp
import asyncio
from time import time
import os
import json

FILE_NAME = 'OLX_ads'
DIR_NAME = "result"
PARSING_DIR = os.path.abspath(os.path.dirname(__name__))
URLS_FILE_PATH = os.path.join(PARSING_DIR, DIR_NAME, f'{FILE_NAME}_URLs.txt')
JSON_OUTPUT_FILE = os.path.join(PARSING_DIR, DIR_NAME, f'{FILE_NAME}.json')
COOKIES = {}
HEADERS = {
    'authority': 'www.olx.ua',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,uk;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': 'mobile_default=desktop; lang=uk; last_locations=58-0-0-%D0%9C%D0%BE%D0%B3%D0%B8%D0%BB%D1%96%D0%B2-%D0%9F%D0%BE%D0%B4%D1%96%D0%BB%D1%8C%D1%81%D1%8C%D0%BA%D0%B8%D0%B9-%D0%92%D1%96%D0%BD%D0%BD%D0%B8%D1%86%D1%8C%D0%BA%D0%B0+%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C-mogilyev%3Apodolskiy; observed_aui=07ca5dd1cb214d81b3d969fe9d12698b; fingerprint=MTI1NzY4MzI5MTs0OzA7MDswOzE7MDswOzA7MDswOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTswOzE7MTsxOzA7MDswOzA7MTswOzA7MTsxOzE7MTsxOzA7MTswOzA7MTsxOzE7MDswOzA7MDswOzA7MTswOzE7MDswOzA7MDswOzA7MTsxOzE7MDsxOzE7MTsxOzA7MTswOzM5NzQwNzk5NDg7MjsyOzI7MjsyOzI7NTsyODQ4MDA2NDE4OzEzNTcwNDE3Mzg7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzA7MDswOzMzOTMxNTk2NTszNDY5MzA2NTUxOzU2NDMzMzYyNjs3ODUyNDcwMjk7MTAwNTMwMTIwMzsxMjgwOzEwMjQ7MjQ7MjQ7MTgwOzEyMDsxODA7MTIwOzE4MDsxMjA7MTgwOzEyMDsxODA7MTIwOzE4MDsxMjA7MTgwOzEyMDsxODA7MTIwOzE4MDsxMjA7MTgwOzEyMDswOzA7MA==; dfp_user_id=cd8da8c9-04c3-4915-a2a8-dc61e0174cfc-ver2; searchFavTooltip=1; laquesisff=aut-388#buy-2279#buy-2811#decision-657#euonb-114#euweb-1372#euweb-451#grw-124#kuna-307#oesx-1437#oesx-2797#oesx-2798#oesx-645#oesx-867#srt-1289#srt-1346#srt-1434#srt-1593#srt-1758#srt-682; laquesissu=299@jobs_cp|0#299@jobs_save_basic_info|0#299@jobs_save_education|0#299@jobs_save_experience|0#299@jobs_save_driving_licence|0#299@jobs_save_language|0#299@jobs_save_interests|0#299@jobs_save_preferred_notifications|0; __utmc=250720985; __gsas=ID=c1312cbb2e9c226d:T=1680687149:S=ALNI_MarZKdJzgkRq9ONtsW7lB2m56Kzzg; _pbjs_userid_consent_data=3524755945110770; __gads=ID=12c19eef2d9f36ef:T=1680687157:S=ALNI_Mb1z0SW0e5J1oEshwlPYca3jzbRXA; lister_lifecycle=1680687162; _hjSessionUser_2218922=eyJpZCI6IjQ2ODBkZWUwLTU2MTEtNTk1Zi04ZTdiLWYxZWNlOWI1YzEzYiIsImNyZWF0ZWQiOjE2ODA2ODcxNTIwMDUsImV4aXN0aW5nIjp0cnVlfQ==; deviceGUID=4cdfb4e4-03ac-44eb-ab00-a6f8d981a83b; a_refresh_token=6c4041a76cad5fab1c26d060422a5c4968acd745; a_grant_type=device; user_id=1052845971; user_business_status=private; cookieBarSeenV2=true; cookieBarSeen=true; _gcl_au=1.1.1279512645.1680702694; delivery_l1=dom-i-sad; PHPSESSID=t861i0l4acmjlqgmltk8ba1845; from_detail=0; laquesis=buy-3321@a#buy-3422@b#de-1282@b#euads-4110@c#fs-1184@b#jobs-5169@b#jobs-5361@a#jobs-5614@b#olxeu-40669@a#olxeu-40670@a#posting-662@b; __utma=250720985.919441558.1680687151.1680687151.1683116863.2; __utmz=250720985.1683116863.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmb=250720985.1.10.1683116863; _gid=GA1.2.42135741.1683116863; _hjIncludedInSessionSample_2218922=0; _hjSession_2218922=eyJpZCI6ImVlYjUxNDI4LTkzMjktNGZmNi04MWZkLTJjNTJhOGQwMzkwZSIsImNyZWF0ZWQiOjE2ODMxMTY4NjM1OTcsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2023-05-03%2015%3A28%3A20%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.ua%2Fd%2Fuk%2Fmogilyev-podolskiy%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.olx.ua%2Fuk%2F; sbjs_first_add=fd%3D2023-05-03%2015%3A28%3A20%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.ua%2Fd%2Fuk%2Fmogilyev-podolskiy%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.olx.ua%2Fuk%2F; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F112.0.0.0%20Safari%2F537.36%20Edg%2F112.0.1722.64; dfp_segment=%5B%5D; my_city_2=58_0_0_%D0%9C%D0%BE%D0%B3%D0%B8%D0%BB%D1%96%D0%B2-%D0%9F%D0%BE%D0%B4%D1%96%D0%BB%D1%8C%D1%81%D1%8C%D0%BA%D0%B8%D0%B9; a_access_token=09e7a283d2cc1c6e116efc49d518fed38bbf9d59; __gpi=UID=00000bd0c55c11e9:T=1680687157:RT=1683116916:S=ALNI_MZY46hy28lsYm2D7LXE8Ok8j2r3dQ; _ga=GA1.1.919441558.1680687151; cto_bundle=gefM4l9HTTElMkJTV2I5VmM2dlBQd3Bnc1BXMHBaVkJNN3dnU0xJZWFNQjNJeWolMkZzODg1bk8lMkJRakQyYWpCWlg3a2I2MXZyRFNwVDJBMnFLTjhXelllRFlNY2I1STY1Q3hDMU5RZ2Y5SldZSUlXbkRxUFBzbUdPTGgwRnBqVW9FJTJGdDFzZ0JyMWJZZHk0SWNkdjNDVnRRJTJCSmslMkZ1ODFZcndCaSUyRlg5dFF1T1FWWkZIa0tlMCUzRA; lqstatus=1683118997|187e1952787x731cd563|buy-3422#euads-4110||; newrelic_cdn_name=CF; sbjs_session=pgs%3D11%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.olx.ua%2Fd%2Fuk%2Fmogilyev-podolskiy%2Fq-%25D0%25A1%25D0%25B0%25D0%25B4%2F; _ga_TVZPR1MEG9=GS1.1.1683116866.3.1.1683118135.60.0.0; session_start_date=1683119947093; onap=18750c2b207x329ed2a3-3-187e1952787x731cd563-39-1683119947',
    'referer': 'https://www.olx.ua/uk/',
    'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64',
}

class OLXPageParser:

    def __init__(self, cookies: dict, headers: dict):
        self.cookies = cookies
        self.headers = headers

    async def get_last_page(self, keyword: str) -> int:
        async with aiohttp.ClientSession() as session:
            url = f'https://www.olx.ua/d/uk/mogilyev-podolskiy/q-{keyword}/'
            async with session.get(url) as response:
                COOKIES.update(response.cookies)
            response = await session.get(url=url, ssl=False, cookies=self.cookies, headers=self.headers)
            soup = bs(await response.text(), "lxml")
            last_page = [i.get('aria-label') for i in soup.find_all('li', {'class': 'pagination-item'})][-1].split()[-1]
            return int(last_page)

    async def get_page_urls(self, keyword:str, page: int):
        async with aiohttp.ClientSession() as session:
            page_url = f'https://www.olx.ua/d/uk/mogilyev-podolskiy/q-{keyword}/?page={page}'
            async with session.get(page_url, cookies=self.cookies, headers=self.headers, ssl=False) as response:
                soup = bs(await response.text(), 'lxml')
                minicards = soup.find_all('div',  class_="css-1sw7q4x")
                all_minicard: bs = (f"https://www.olx.ua/{i.find('a').get('href')}" for i in minicards[:-1])
                return all_minicard

    async def get_all_page_urls(self, keyword):
        last_page = await self.get_last_page(keyword)
        fetch_page_tasks = (self.get_page_urls(keyword, i) for i in range(1, int(last_page)+1))
        page_results = await asyncio.gather(*fetch_page_tasks)
        articles_urls_list = [item for sublist in page_results for item in sublist]
        return set(articles_urls_list)


class URLSaver:

    def __init__(self, dir_name):
        self.dir_name = dir_name

    def save_urls_to_file(self, urls_list):
        os.makedirs(self.dir_name, exist_ok=True)
        with open(os.path.join(self.dir_name, f'{FILE_NAME}_URLs.txt'), 'w', encoding='UTF-8') as file:
            [file.write(f"{url}\n") for url in urls_list]



class AdsParser:
    def __init__(self, ads_url_list: str, output_file_path: str, headers: str, cookies: str):
        self.ads_url_list = ads_url_list
        self.output_file_path = output_file_path
        self.HEADERS = headers
        self.COOKIES = cookies

    async def run(self) -> list:
        urls = self._read_urls_file()
        async with aiohttp.ClientSession(headers=self.HEADERS, cookies=self.COOKIES) as session:
            tasks = []
            for url in urls:
                tasks.append(asyncio.ensure_future(self._parse_post_data(session, url)))
            results = await asyncio.gather(*tasks)
            self._save_results(results)

    def _read_urls_file(self) -> list:
        with open(self.ads_url_list, encoding="UTF-8") as file:
            return [url.strip() for url in file.readlines()]

    async def _parse_post_data(self, session: aiohttp.ClientSession, url: str) -> dict:
        async with session.get(url) as response:
            ad_html = await response.text()
            soup = bs(ad_html, 'lxml')
            try:
                ads_title = soup.find('h1').text.strip()
            except:
                ads_title = None
            try:
                ads_price = soup.find('h3', class_="css-ddweki er34gjf0").text.strip()
            except:
                ads_price = None
            try:
                ads_date = soup.find('span', class_='css-19yf5ek').text.strip()
            except:
                ads_date = None
            try:
                ads_description = soup.find('div', class_="css-bgzo2k").text.strip()
            except:
                ads_description = None
            try:
                all_photo_blocks = soup.find_all('div', class_='swiper-slide css-1915wzc')
                ads_photo_urls = [i.find('div', class_="swiper-zoom-container").find('img').get('src').strip()
                                for i in all_photo_blocks]
            except:
                ads_photo_urls = None
            try:
                seller_name = soup.find('h4', class_="css-1lcz6o7").text.split()
            except:
                seller_name = None
            return {
                "original_url": url,
                "ads_date": ads_date,
                "ads_title":ads_title,
                "ads_photo_urls": ads_photo_urls,
                "ads_price": ads_price,
                "ads_description": ads_description,
                "seller_name": " ".join(seller_name),
            }

    def _save_results(self, results: list) -> json:
        with open(self.output_file_path, 'w', encoding='UTF-8') as file:
            json.dump(results, file, indent=4, ensure_ascii=False)
        print(f'{len(results)} ads were received. They were saved in the file {self.output_file_path}.')



async def main():

    keyword = "Сад"
    parser = OLXPageParser(COOKIES, HEADERS)
    saver = URLSaver(DIR_NAME)
    urls_list = await parser.get_all_page_urls(keyword)
    saver.save_urls_to_file(urls_list)
    ads_parser = AdsParser(URLS_FILE_PATH, JSON_OUTPUT_FILE, HEADERS, COOKIES)

    await ads_parser.run()


if __name__ == "__main__":

    x = time()
    asyncio.run(main())
    y = time()
    print(round(y-x, 2))