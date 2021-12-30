from __future__ import annotations

from asyncio import gather, run
from dataclasses import dataclass, field
from time import time
from typing import Optional

from aiohttp.client import ClientSession
from aiopath import AsyncPath
from bs4 import BeautifulSoup as Soup
from bs4.element import NavigableString, Tag
from yarl import URL

from config import Config, Params


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

    async def fetch(self, url: str):
        async with self.session.get(url) as res:
            soup = Soup(await res.text(), "html.parser")
            anchors = soup.find_all("a", href=True)
            imgs = [a["href"] for a in anchors if a.find("img")]
            print(imgs)

    async def initlinks(self):
        url, params = self.config.baseurl, self.config.params
        async with self.session.get(url, params=params) as res:
            soup = Soup(await res.text(), "html.parser")
            # anchors = soup.find_all("a", href=True)
            # imgs = [a["href"] for a in anchors if a.find("img")]

        alt = soup.find("a", alt="last page")
        if not alt:
            return
        # print(alt["href"], self.config.baseurl)
        last = URL(alt["href"])
        print(last.query_string)
        params = "&".join(
            [f"{k}={v}" for k, v in last.query.items() if k != "pid"]
        )

        pid = last.query["pid"]  # type: ignore
        pids = [i * 40 for i in range(1, int(pid) // 40)]
        links = [f"{url}?{params}&pid={pid}" for pid in pids]
        await gather(*[self.fetch(link) for link in links])
        # print(pids)
        # print(imgs)
        # for a in :
        #     print(a["href"])

        # return [a["href"] for a in links]

    async def fetch_all(self):
        ...
        # async with self.session(loop=loop)

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
    config = Config("touhou 1girl scenery")

    async with ClientSession() as session:
        downloader = Engine(session, config)
        print(await downloader.initlinks())
        # await downloader.save(test_url)  # "https://www.google.com"


run(main())
