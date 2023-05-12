import time
from aiohttp import ClientSession
import asyncio


async def get_items(session: ClientSession, url: str, discount: int) -> list[dict]:
    """Получает данные о предметах на странице по заданному URL-адресу
    Args:
        session (ClientSession): Сессия aiohttp, используемая для выполнения запроса
        url (str): URL-адрес, на который нужно выполнить запрос
    Returns:
        list[dict]: Список словарей, каждый из которых содержит информацию о предмете
    """
    async with session.get(url) as response:
        data: dict = await response.json()  # извлечение JSON-данных из ответа
        items = data.get('items')  #  извлечение списка предметов из словаря "data"
        result = []
        for i in items:
            if i["pricing"]["discount"] is not None and i["pricing"]["discount"] >= float(f"0.{discount}"):
                item_name = i["asset"]["names"]["full"]
                try:
                    item_3d = i["links"]["3d"]
                except:
                    item_3d = None
                item_price = f'{i["pricing"]["computed"]} $'
                item_discount = (f'{round(i["pricing"]["discount"]*100, 2)} %')
                result.append({"item_name": item_name,
                               "item_3d": item_3d,
                               "item_discount": item_discount,
                               "item_price":item_price})
        return result

async def csgo_parser(category: int = 2, discount:int = 10, min:int=2000, max:int=10_000) -> list[dict]:
    """Эта функция асинхронно парсит сайт cs.money для получения списка элементов CS:GO с заданными параметрами.
    Args:
        category (int, optional): категория элементов CS:GO (1 - скины, 2 - ножи и т. д.). Defaults to 2.
        discount (int, optional): минимальный порог скидки при поиске. Defaults to 10.
        min (int, optional): минимальный порог цены. Defaults to 2000.
        max (int, optional): максимальный порог цены. Defaults to 10_000.
    Returns:
        list[dict]: список словарей, содержащих данные об элементах CS:GO.
    """
    result = []  # создание пустого списка для хранения данных об элементах CS:GO
    offset = 0  # начальное смещение списка элементов
    step_size = 60  # размер шага для получения списка элементов

    async with ClientSession() as session:  # создание асинхронной сессии для запросов
        tasks = []  # создание пустого списка для хранения задач на получение элементов CS:GO
        while True:
            for item in range(offset, offset+step_size, 60):  # проход по списку элементов
                url = f"https://cs.money/1.0/market/sell-orders?limit=60&minPrice={min}&maxPrice={max}&sort=discount&offset={item}&type={category}"
                task = asyncio.create_task(get_items(session, url, discount))  # создание задачи на получение элементов
                tasks.append(task)  # добавление задачи в список задач
                offset += step_size  # смещение списка элементов на заданный шаг
            if not tasks: break  # если список задач пуст, то выход из цикла
            items = await asyncio.gather(*tasks)  # ожидание завершения всех задач
            for i in items: result += i  # добавление полученных элементов в список элементов
            tasks = []  # очистка списка задач
            if len(items) < 60: break  # если получено менее 60 элементов, то выход из цикла

    return result  # возврат списка элементов

if __name__ == "__main__":
    x = time.time()
    asyncio.run(csgo_parser())
    y = time.time()
    print(y-x)