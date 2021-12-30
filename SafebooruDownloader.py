#!/usr/bin/env python3

from __future__ import annotations
import asyncio

from dataclasses import dataclass, field
from pathlib import Path
from re import findall
from typing import Generator, AsyncGenerator

import bs4
import requests
from bs4 import BeautifulSoup as Soup


@dataclass
class Config:
    raw_tags: str = field(repr=False)
    path: Path = field(default_factory=Path)
    baseurl: str = field(init=False, repr=False)
    tags: list[str] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.tags = self.raw_tags.split(" ")
        if self.path == Path():
            self.path /= "img"
        self.path /= "-".join(self.tags)
        self.baseurl = (
            "http://safebooru.org/index.php?page=post&s=list&"
            f"tags={self.raw_tags}"
        )


def get_next_page(page, url):
    """Get the next page. Returns None if it is the last page."""
    nextSoup = page.find("a", alt="next")
    if nextSoup is None:
        return None
    else:
        nextUrl = url + "index.php" + nextSoup.get("href")
    return requests.get(nextUrl)


class Downloader:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.pages: list[Page] = [Page(self.config.baseurl)]
        self.config.path.mkdir(parents=True, exist_ok=True)

    async def download_image(self, url: str):
        """Save an image from a URL to a new directory."""
        image = requests.get(url)
        img_id = url.split('?').pop()
        filetype = image.headers["content-type"].split("/")[-1]
        path = (self.config.path / img_id).with_suffix("." + filetype)
        path.write_bytes(image.content)

    def run(self):
        p = self.pages[0]
        # download_links = (Downloader.get_image(l) for l in self.pages[0].links)
        # await asyncio.gather([self.download_image(l) for l in p.links_dl])
        # for l in p.links_dl:
        #     print(l)
        #     await self.download_imaged(l)

        # print(f"downloaded {len(p.links)} images from {len(self.pages)} pages")
        # print([])
        ...
        # while True:
        # ...
        # self.Page.append(Page(self.get_image_links()))


@dataclass
class Page:
    url: str
    soup: Soup = field(init=False, repr=False)
    links: list[str] = field(init=False, repr=False)
    # links_dl: AsyncGenerator[str, None] = field(init=False, repr=False)
    # ids: list[str] = field(init=False)

    def __post_init__(self):
        self.soup = Page.get_soup(self.url, strict=True)
        self.links = self.get_image_links()
        # self.links_dl = self.gen_image_links_download()
        # self.ids = self.get_ids()

    @staticmethod
    def get_soup(url: str, *, strict: bool = False) -> Soup:
        res = requests.get(url)
        if strict and "Nothing found" in res.text:
            raise ValueError("No images found, check your tags?")
        return Soup(res.text, features="html.parser")

    def get_image_links(self):
        links = self.soup.find_all("a")
        return [
            self.url + link.get("href") for link in links if link.find("img")
        ]

    # async def gen_image_links_download(self):
    #     for link in self.links:
    #         image = Page.get_soup(link).find(id="image")
    #         if isinstance(image, bs4.element.Tag):
    #             res = image.get("src")
    #             if isinstance(res, list):
    #                 for l in res:
    #                     yield l
    #             elif res:
    #                 yield res

    # @staticmethod
    # def get_id(url: str) -> str | None:
    #     res = findall(r"(?<=\&id=)\d*", url)
    #     return res.pop() if res else None

    # def get_ids(self):
    #     ids = [Page.get_id(l) for l in self.links]
    #     return [i for i in ids if i is not None]

async def get_soup(url: str, *, strict: bool = False) -> Soup:
    res = requests.get(url)
    if strict and "Nothing found" in res.text:
        raise ValueError("No images found, check your tags?")
    return Soup(res.text, features="html.parser")

async def main():
    # page = Page("http://safebooru.org/index.php?page=post&s=list&tags=touhou")
    # raw_tags = input("Enter tags separated by spaces\n")
    # path = Path()
    # path = Path(input("Enter download path, blank for cwd\n"))
    # config = Config(raw_tags=raw_tags, path=path)
    # print(config.baseurl)
    # downloader = Downloader(config)
    # downloader.run()
    # exit()
    # while True:
    #     # Next Page
    #     res = get_next_page(soup, url)
    #     if res is None:
    #         print(f"Finished! Downloaded {imagescount} images!")
    #         break

    #     pagecount += 1


if __name__ == "__main__":
    asyncio.run(main())
