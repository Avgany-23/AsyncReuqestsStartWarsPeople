import aiohttp
import certifi
import asyncio
import ssl


ssl_context = ssl.create_default_context(cafile=certifi.where())


class ParsePeopleData:
    def __init__(self, data: dict) -> None:
        self.poles = ['title', 'name', 'name', 'name']
        self.type_info = ['films', 'species', 'vehicles', 'starships']
        self.data = self.deleted_poles(data)

    @staticmethod
    def deleted_poles(data: dict) -> dict:
        for delete in ('created', 'edited', 'url'):
            data.pop(delete, None)
        return data

    @staticmethod
    def join_func(data: list[tuple[str, str]], type_info: str) -> str:
        """Функция отбирает все значения из data, первый элемент кортежа которых равен type_info"""
        filter_data = filter(lambda x: x[0] == type_info, data)
        result_data = ','.join(type_info[1] for type_info in filter_data)
        return result_data

    @staticmethod
    async def find_info_about_person(url: str, pole: str, type_info: str) -> tuple[str, str]:
        conn = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=conn) as client:
            async with client.get(url) as response:
                data = await response.json()
                return type_info, data[pole]

    async def get_parse_data(self) -> dict:
        tasks = []
        for pole, type_ in zip(self.poles, self.type_info):
            for key in self.data[type_]:
                tasks.append(self.find_info_about_person(key, pole, type_))
        info_about_person = await asyncio.gather(*tasks)
        for type_ in self.type_info:
            self.data[type_] = self.join_func(info_about_person, type_)
        return self.data
