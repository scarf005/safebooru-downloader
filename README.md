# Safebooru Downloader

Downloads all images available with matching tags from Safebooru

original script from [@PRISISM](https://github.com/PRISISM/safebooru-downloader), rewritten from scratch using python's asynchronous modules

[`asyncio`](https://docs.python.org/3/library/asyncio.html), [`aiohttp`](https://github.com/aio-libs/aiohttp), [`aiopath`](https://github.com/alexdelorenzo/aiopath)

to concurrently download images in bulk.

`usage: run.py [-h] [-p PATH] tags [tags ...]`

# What's changed

benchmark using 5 tags:

```py
[39 images]
with async: 4.7seconds
without async: 108.8seconds
2314%
```

## TODO

- program downloads image first then checks if there are duplicates
- package into working module