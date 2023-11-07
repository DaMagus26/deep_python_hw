import asyncio
import logging
import argparse
import os
from collections import Counter
import json
from typing import Optional, IO
from bs4 import BeautifulSoup
import aiohttp


async def fetch_url(
        url: str
) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                return ''
    except AssertionError:
        logging.error(f'AssertionError caught: {url}')
        return None


async def fetch_worker(
        que: asyncio.Queue
) -> None:
    while True:
        url = await que.get()
        if url is None:
            await que.put(url)
            break

        response = await fetch_url(url)
        result = parse_page(response)
        print(f'{url}: {result}')


async def batch_fetch(
        file: str | IO,
        num_workers: int
) -> None:
    queue = asyncio.Queue(maxsize=num_workers * 2)

    if not isinstance(num_workers, int):
        raise TypeError('num_workers must be integer')
    if num_workers < 1:
        raise ValueError("num_workers must be at least 1")

    workers = [
        fetch_worker(queue) for _ in range(num_workers)
    ]

    await asyncio.gather(fill_queue(queue, file), *workers)


async def fill_queue(
        queue: asyncio.Queue,
        file: str | IO,
) -> None:
    if isinstance(file, str) and not os.path.exists(file):
        raise OSError('No such path:', file)
    with (open(file, 'r', encoding='UTF-8')
          if isinstance(file, str) else file as file_obj):
        for url in file_obj:
            await queue.put(url.strip())
        await queue.put(None)


def parse_page(
        text: str | None
) -> str:
    if text is None:
        return json.dumps({
            '$error': 'Could not connect to page'
        })

    if text == '':
        return json.dumps({
            '$error': 'Status code is not 200'
        })

    soup = BeautifulSoup(text, "html.parser")
    mcw = most_common_words(soup)
    return json.dumps(mcw)


def most_common_words(
        soup: BeautifulSoup,
        top_k: int = 7
) -> dict:
    words = soup.get_text().split()
    counter = Counter(words)
    return dict(counter.most_common(top_k))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(prog="Async fetcher")
    parser.add_argument("-c", type=int)
    parser.add_argument("-p", default='urls.txt', type=str)
    arguments = parser.parse_args()

    try:
        asyncio.run(batch_fetch(arguments.p, arguments.c))
    except KeyboardInterrupt:
        logging.info('Execution interrupted by user')
