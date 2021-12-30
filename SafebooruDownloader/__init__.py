from asyncio import run
from dataclasses import dataclass, field
from typing import Optional

from aiohttp.client import ClientSession
from aiopath import AsyncPath
from bs4 import BeautifulSoup as Soup

from config import Config

class Engine:
    def __init__(self, session: ClientSession, config: Config) -> None:
        self.session = session
        self.config = config
        self.path = AsyncPath("img")

    async def save(self, url: str):
        async with self.session.get(url) as res:
            ext = res.headers["content-type"].split("/").pop()
            path = (self.path / res.url.query_string).with_suffix(f".{ext}")
            if not await path.exists():
                await path.write_bytes(await res.read())

    async def getlinks(self):
        ...

    #     print(img.headers.get("content-type"))
    #     print(img.status)
    # async def download_image(self, url: str):
    #     """Save an image from a URL to a new directory."""
    #     image = requests.get(url)
    #     img_id = url.split('?').pop()
    #     filetype = image.headers["content-type"].split("/")[-1]
    #     path = (self.config.path / img_id).with_suffix("." + filetype)
    #     path.write_bytes(image.content)


test_url = "https://safebooru.org//samples/3598/sample_a406fd8bba13072c4c3db4ceb803821ed059c920.jpg?3758206"


async def main():
    config = Config("touhou scenery")
    print(config)
    exit()

    async with ClientSession() as session:
        downloader = Engine(session, config)
        await downloader.save(test_url)  # "https://www.google.com"
        # await downloader.save()


run(main())
