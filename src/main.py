from copy_contents import copy_contents
from generate_page import generate_page_r
from textnode import TextNode


def main():
    copy_contents("static/", "public/")
    generate_page_r("content/", "template.html", "public/")


main()
