#!/usr/bin/env python3

import os

import bs4
import requests
from bs4 import BeautifulSoup as Soup

""" Safebooru Downloader

Downloads all images available of selected tags from http://safebooru.org/

Author: toashel @ http://github.com/toashel
"""


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


def get_image_links(page: Soup, url: str, pagecount) -> list[str]:
    """Get all image links on a page."""
    print(f"Getting image links for Page {pagecount}...")
    links = page.find_all("a")
    imageLinks = [url + link.get("href") for link in links if link.find("img")]
    return imageLinks


def get_next_page(page, url):
    """Get the next page. Returns None if it is the last page."""
    nextSoup = page.find("a", alt="next")
    if nextSoup is None:
        return None
    else:
        nextUrl = url + "index.php" + nextSoup.get("href")
    return requests.get(nextUrl)


def main():
    url = "http://safebooru.org/"

    userSearch: str = input(
        "What tags are you searching for?\nEnter them all separated by spaces!\n\n"
    )
    userURL: str = (
        f"http://safebooru.org/index.php?page=post&s=list&tags={userSearch}"
    )

    path = "safeboorudownloader/" + userSearch
    os.makedirs(path, exist_ok=True)
    # store images in a directory named after search

    imagescount = 0
    pagecount = 1
    res = requests.get(userURL)  # page 1

    if "Nothing found" in res.text:
        print("No images found, check your tags?")
        return

    while True:
        soup = bs4.BeautifulSoup(res.text)

        # array of links to images
        imageLinks = get_image_links(soup, url, pagecount)
        imagescount += len(imageLinks)

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
