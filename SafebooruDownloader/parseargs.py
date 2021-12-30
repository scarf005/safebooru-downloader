from argparse import ArgumentParser

from aiopath.path import AsyncPath

parser = ArgumentParser(description="Download images from safebooru")
parser.add_argument("tags", nargs="+", help="tags to search for")
parser.add_argument(
    "-p", "--path", default="img", type=AsyncPath, help="path to save images"
)

args = parser.parse_args()
