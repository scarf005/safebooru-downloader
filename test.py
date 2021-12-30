import asyncio

from aiohttp import ClientSession


async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()
            print(response)

asyncio.run(hello("http://httpbin.org/headers"))
