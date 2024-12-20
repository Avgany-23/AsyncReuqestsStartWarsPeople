from utils import save_data_to_db, initial_models
from utils.parse import ParsePeopleData, ssl_context
from time import time
import asyncio
import aiohttp
import logging


async def get_people_request(id_user: int, semaphore: asyncio.Semaphore) -> dict:
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    async with semaphore, aiohttp.ClientSession(connector=conn) as client:
        url = 'https://swapi.py4e.com/api/people/%s/' % id_user
        async with client.get(url) as response:
            data = await response.json()
            if data == {'detail': 'Not found'}:
                return dict()
            parse_data = ParsePeopleData(data)
            result = await parse_data.get_parse_data()
            result.update(id_character=id_user)
            return result


async def main(count: int = 100, timeout_requests: float = 15, semaphore: int = 50) -> None:
    semaphore = asyncio.Semaphore(value=semaphore)
    tasks = [asyncio.create_task(get_people_request(id_user, semaphore)) for id_user in range(1, count + 1)]
    start_time = time()
    done, pending = await asyncio.wait(tasks, timeout=timeout_requests, return_when=asyncio.FIRST_EXCEPTION)

    await initial_models()
    await save_data_to_db([d.result() for d in done if d.result()])

    logging.log(
        level=logging.INFO,
        msg='Кол-во записанных записей - %s из %s:Пройденное время: %sс.' %
            (sum(map(lambda task: bool(task.result()), done)), len(done), round(time() - start_time, 2))
    )
    if (count_pending := len(pending)) > 0:
        logging.log(
            level=logging.WARNING,
            msg='Кол-во ожидающих задач - %s' % count_pending
        )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(count=100, timeout_requests=10))
