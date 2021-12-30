from time import time
from SafebooruDownloader.__init__ import main
from asyncio import run

s = time()
run(main())
e = time()
print(f"took {(e - s) * 1000}ms")

