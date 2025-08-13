import re

from textnode import TextNode, TextType, split_nodes_delimiter


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_images(old_node.text)
            if matches is None:
                new_nodes.append(old_node)
            else:
                remaining_text = old_node.text
                for match in matches:
                    image_alt = match[0]
                    image_link = match[1]
                    sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
                    text_before = sections[0]
                    if text_before:
                        new_nodes.append(TextNode(text_before, TextType.TEXT, None))
                    remaining_text = sections[1] if len(sections) > 1 else ""
                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT, None))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_links(old_node.text)
            if matches is None:
                new_nodes.append(old_node)
            else:
                remaining_text = old_node.text
                for match in matches:
                    link_alt = match[0]
                    link_link = match[1]
                    sections = remaining_text.split(f"[{link_alt}]({link_link})", 1)
                    text_before = sections[0]
                    if text_before:
                        new_nodes.append(TextNode(text_before, TextType.TEXT, None))
                    remaining_text = sections[1] if len(sections) > 1 else ""
                    new_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT, None))
    return new_nodes


def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]

    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes


def extract_title(markdown):

    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()  # Return title without the "# "
            break
    raise ValueError("No title found in the markdown text.")
