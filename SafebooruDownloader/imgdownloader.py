from __future__ import annotations

from asyncio import gather
from pathlib import Path

from aiohttp.client import ClientSession
from bs4 import BeautifulSoup as Soup
from bs4.element import Tag
from termcolor import cprint

from .config import Config


class ImageDownloader:
    def __init__(self, session: ClientSession, config: Config):
        self.session = session
        self.config = config
        self.mkdir()

    def mkdir(self):
        path = Path(self.config.path)
        if not path.exists():
            path.mkdir(parents=True)

    async def save(self, url: str):
        async with self.session.get(url) as res:
            soup = Soup(await res.text(), "html.parser")
            img = soup.find(id="image")
            if not isinstance(img, Tag):
                return

        src = img["src"]
        async with self.session.get(src) as res:  # type: ignore
            basepath, imgid = self.config.path, res.url.query_string
            ext = res.headers["content-type"].split("/").pop()
            path = (basepath / imgid).with_suffix(f".{ext}")
            if await path.exists():
                cprint(f"⏭️  exsisting img: {imgid}", "yellow")
            else:
                await path.write_bytes(await res.read())
                cprint(f"✅  download  img: {imgid}", "green")

    # search through page url and downloads all images
    async def download(self, soup: Soup) -> None:
        anchors = soup.find_all("a", href=True)
        imgs = [
            f"{self.config.baseurl}/{a['href']}"
            for a in anchors
            if a.find("img")
        ]
        await gather(*[self.save(img) for img in imgs])
