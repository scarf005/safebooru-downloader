from dataclasses import dataclass, field
from aiopath import AsyncPath

@dataclass
class Config:
    _raw_tags: str = field(repr=False)
    path: AsyncPath = field(default=AsyncPath("img"))
    tags: list[str] = field(init=False)
    baseurl: str = field(init=False, repr=False)
    params: dict[str, str] = field(init=False, repr=False)

    def __post_init__(self):
        self.tags = self._raw_tags.split(" ")
        self.path /= "-".join(self.tags)
        self.baseurl = "http://safebooru.org/index.php?page=post"
        self.params = {"s": "list", "tags": "+".join(self.tags)}

