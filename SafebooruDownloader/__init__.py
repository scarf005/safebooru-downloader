from __future__ import annotations

from asyncio import gather, run

from aiohttp.client import ClientSession
from bs4 import BeautifulSoup as Soup
from multidict import MultiDict
from termcolor import cprint
from yarl import URL

from .config import Config
from .imgdownloader import ImageDownloader
from .parseargs import args


class Engine:
    def __init__(self, session: ClientSession, config: Config) -> None:
        self.session = session
        self.config = config
        self.imgdl = ImageDownloader(session, config)

    # called page search
    async def fetch(self, url: str) -> None:
        async with self.session.get(url) as res:
            await self.imgdl.download(Soup(await res.text(), "html.parser"))

    # inital page search, asyncrhonously loads all pages
    async def fetch_all(self) -> None:
        async def get_links(q: MultiDict) -> list[str]:
            params = "&".join([f"{k}={v}" for k, v in q.items() if k != "pid"])
            pids = [i * 40 for i in range(1, int(q["pid"]) // 40)]
            links = [f"{url}?{params}&pid={pid}" for pid in pids]
            return links

        url, params = self.config.baseurl, self.config.params
        async with self.session.get(url, params=params) as res:
            text = await res.text()
            if "Nothing found" in text:
                input_param = ", ".join(f"<{t}>" for t in self.config.tags)
                cprint(f"🚫 No result, please check tags {input_param}", "red")
                await self.config.path.rmdir()
                return

            soup = Soup(text, "html.parser")
            await self.imgdl.download(soup)
            alt = soup.find("a", alt="last page")
            if not alt:
                print(f"📄 1 page found")

        tags = URL(alt["href"]).query  # type: ignore
        links = await get_links(tags)
        await gather(*[self.fetch(link) for link in links])
        print(f"📑 {len(links) + 1} pages found")


async def main(config: Config):
    async with ClientSession() as session:
        downloader = Engine(session, config)
        return await downloader.fetch_all()


if __name__ == "__main__":
    config = Config(args.tags, path=args.path)
    run(main(config))
