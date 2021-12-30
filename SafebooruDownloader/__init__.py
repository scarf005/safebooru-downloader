from __future__ import annotations

from asyncio import gather, run
from dataclasses import dataclass, field
from pathlib import Path
from time import time
from typing import Optional

from aiohttp.client import ClientSession
from aiohttp.client_reqrep import ClientResponse
from aiopath import AsyncPath
from bs4 import BeautifulSoup as Soup
from bs4.element import NavigableString, Tag
from multidict import MultiDict
from yarl import URL

from config import Config, Params


class Engine:
    def __init__(self, session: ClientSession, config: Config) -> None:
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
            basepath = self.config.path
            ext = res.headers["content-type"].split("/").pop()
            path = (basepath / res.url.query_string).with_suffix(f".{ext}")
            if not await path.exists():
                await path.write_bytes(await res.read())

    # search through page url and downloads all images
    async def download(self, soup: Soup) -> None:
        anchors = soup.find_all("a", href=True)
        imgs = [
            f"{self.config.baseurl}/{a['href']}"
            for a in anchors
            if a.find("img")
        ]

        # download images using url with async
        await self.save(imgs[1])
        print(imgs[1])

    # called page search
    async def fetch(self, url: str) -> None:
        async with self.session.get(url) as res:
            await self.download(Soup(await res.text(), "html.parser"))

    # inital page search, asyncrhonously loads all pages
    async def fetch_all(self) -> None:
        async def get_links(q: MultiDict) -> list[str]:
            params = "&".join([f"{k}={v}" for k, v in q.items() if k != "pid"])
            pids = [i * 40 for i in range(1, int(q["pid"]) // 40)]
            links = [f"{url}?{params}&pid={pid}" for pid in pids]
            return links

        url, params = self.config.baseurl, self.config.params
        async with self.session.get(url, params=params) as res:
            soup = Soup(await res.text(), "html.parser")
            await self.download(soup)
            alt = soup.find("a", alt="last page")
            if not alt:
                return

        tags = URL(alt["href"]).query  # type: ignore
        await gather(*[self.fetch(link) for link in await get_links(tags)])


test_url = "https://safebooru.org//samples/3598/sample_a406fd8bba13072c4c3db4ceb803821ed059c920.jpg?3758206"


async def main():
    config = Config("touhou 1girl scenery bird")  #

    async with ClientSession() as session:
        downloader = Engine(session, config)
        await downloader.fetch_all()


run(main())
