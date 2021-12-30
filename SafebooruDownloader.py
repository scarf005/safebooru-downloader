#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from re import findall
from typing import Generator

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


@dataclass
class Images:
    ...


def download_image(url, directory: str):
    """Save an image from a URL to a new directory."""
    image = requests.get(url)
    filetype = image.headers["content-type"].split("/")[-1]
    name = directory + "/" + url.split("?")[1] + "." + filetype

    with open(name, "wb") as f:
        f.write(image.content)


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
        self.images = Images()
        self.pages: list[Page] = [Page(self.config.baseurl)]
        self.config.path.mkdir(parents=True, exist_ok=True)

    def run(self):
        # download_links = (Downloader.get_image(l) for l in self.pages[0].links)
        for l in self.pages[0].links_download:
            print(l)
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
    links_download: Generator[str, None, None] = field(init=False, repr=False)
    ids: list[str] = field(init=False)

    def __post_init__(self):
        self.soup = Page.get_soup(self.url, strict=True)
        self.links = self.get_image_links()
        self.ids = self.get_ids()
        self.links_download = self.gen_image_links_download()

    @staticmethod
    def get_soup(url, *, strict: bool = False) -> Soup:
        res = requests.get(url)
        if strict and "Nothing found" in res.text:
            raise ValueError("No images found, check your tags?")
        return Soup(res.text, features="html.parser")

    def get_image_links(self) -> list[str]:
        links = self.soup.find_all("a")
        return [
            self.url + link.get("href") for link in links if link.find("img")
        ]

    # generator
    # def get_image(url) -> str | list[str] | None:
    def gen_image_links_download(self):
        for link in self.links:
            image = Page.get_soup(link).find(id="image")
            # imagePage = requests.get(link)
            # imageSoup = bs4.BeautifulSoup(imagePage.text, features="html.parser")
            # image = imageSoup.find(id="image")
            if isinstance(image, bs4.element.Tag):
                res = image.get("src")
                if isinstance(res, list):
                    yield from res
                else:
                    yield res

    @staticmethod
    def get_id(url) -> str | None:
        res = findall(r"(?<=\&id=)\d*", url)
        return res.pop() if res else None

    def get_ids(self):
        ids = [Page.get_id(l) for l in self.links]
        return [i for i in ids if i is not None]


def main():
    raw_tags = input("Enter tags separated by spaces\n")
    path = Path(input("Enter download path, blank for cwd\n"))
    config = Config(raw_tags=raw_tags, path=path)
    downloader = Downloader(config)
    downloader.run()
    exit()
    while True:
        print("Getting images, this might take a while...")
        images = [
            get_image(link) for link in imageLinks
        ]  # array of image links

        for _ in range(images.count(None)):
            images.remove(None)

        for imageLink in images:
            print(imageLink, end="")
            download_image(imageLink, path)
            print(" Done!")

        # Next Page
        res = get_next_page(soup, url)
        if res is None:
            print(f"Finished! Downloaded {imagescount} images!")
            break

        pagecount += 1


if __name__ == "__main__":
    main()
