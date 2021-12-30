from dataclasses import dataclass, field

from aiopath import AsyncPath
from yarl import URL

Params = dict[str, str]

@dataclass
class Config:
    _raw_tags: str = field(repr=False)
    path: AsyncPath = field(default=AsyncPath("img"))
    tags: list[str] = field(init=False)
    baseurl: URL = field(init=False, repr=False)
    params: Params = field(init=False, repr=False)

    def __post_init__(self):
        self.tags = self._raw_tags.split(" ")
        self.path /= "-".join(self.tags)
        self.baseurl = URL("http://safebooru.org/index.php?page=post")
        self.params = {"s": "list", "tags": self._raw_tags}
