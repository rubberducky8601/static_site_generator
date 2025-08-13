import sys

from copy_contents import copy_contents
from generate_page import generate_page_r
from textnode import TextNode


def main():
    if len(sys.argv) > 2:
        exit("Usage: python main.py [basepath]")
    basepath = sys.argv[1]

    copy_contents(basepath, "docs/")
    generate_page_r(basepath, "template.html", "docs/")


main()
