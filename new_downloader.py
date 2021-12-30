import asyncio
import aiohttp
import aiofiles
from aiopath import AsyncPath
from aiohttp.client import ClientSession
from bs4 import BeautifulSoup as Soup

class Downloader:
    def __init__(self, session) -> None:
        self.session = session
        self.path = AsyncPath("img")

    async def download(self, url: str):
        async with self.session.get(url) as res:
            print(res.url)
            print("Status:", res.status)
            print("Content-type:", res.headers['content-type'])

            html = await res.text()
            print("Body:", html[:15], "...")

    # async def save(self):
    #     img = await self.download("http://httpbin.org/headers")

    #     path = self.path / "abc"
    #     if await path.exists():
    #         return
    #     print(img.headers.get("content-type"))
    #     print(img.status)
    # async def download_image(self, url: str):
    #     """Save an image from a URL to a new directory."""
    #     image = requests.get(url)
    #     img_id = url.split('?').pop()
    #     filetype = image.headers["content-type"].split("/")[-1]
    #     path = (self.config.path / img_id).with_suffix("." + filetype)
    #     path.write_bytes(image.content)

async def main():
    async with ClientSession() as session:
        downloader = Downloader(session)
        await downloader.download("https://www.google.com")
        # await downloader.save()


asyncio.run(main())