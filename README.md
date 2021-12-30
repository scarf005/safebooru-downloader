# Safebooru Downloader

Downloads all images available with matching tags from Safebooru
forked from [@PRISISM](https://github.com/PRISISM/safebooru-downloader)

## What's changed

uses python's asynchronous modules, namely

[`asyncio`](https://docs.python.org/3/library/asyncio.html), [`aiohttp`](https://github.com/aio-libs/aiohttp), [`aiopath`](https://github.com/alexdelorenzo/aiopath)

to concurrently download images in bulk.

benchmark using 5 tags:

```py
[39 images]
with async: 4.7seconds
without async: 108.8seconds
speed difference: 2314%
```

## TODO

program downloads image first then checks if there are duplicates