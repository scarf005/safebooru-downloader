#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from re import findall

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


def get_image(url):
    """Get the image from a url."""
    imagePage = requests.get(url)
    imageSoup = bs4.BeautifulSoup(imagePage.text, features="html.parser")
    image = imageSoup.find(id="image")
    if image:
        return image.get("src")


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
        self.Page: list[Page] = [Page(self.config.baseurl)]
        self.config.path.mkdir(parents=True, exist_ok=True)

    def run(self):
        print(self.Page)
        ...
        # while True:
        # ...
        # self.Page.append(Page(self.get_image_links()))


@dataclass
class Page:
    url: str
    soup: Soup = field(init=False, repr=False)
    links: list[str] = field(init=False, repr=False)
    ids: list[str] = field(init=False)

    def __post_init__(self):
        self.soup = self.get_soup()
        self.links = self.get_image_links()
        self.ids = self.get_ids()

    def get_soup(self) -> Soup:
        res = requests.get(self.url)
        if "Nothing found" in res.text:
            raise ValueError("No images found, check your tags?")
        return Soup(res.text, features="html.parser")

    def get_image_links(self) -> list[str]:
        links = self.soup.find_all("a")
        return [
            self.url + link.get("href") for link in links if link.find("img")
        ]

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
    imagescount = 0
    pagecount = 1

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
