import unittest

from extract_markdown import (extract_markdown_images, extract_markdown_links,
                              text_to_textnodes)
from textnode import (TextNode, TextType, split_nodes_delimiter,
                      text_node_to_html_node)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "URL")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_equal_property(self):
        node = TextNode("This is a text node", TextType.CODE, "URL")
        node2 = TextNode("This is a text node", TextType.CODE, "URL")
        self.assertEqual(node, node2)

    def test_not_equal_property(self):
        node = TextNode("This is a text node", TextType.CODE, "URL")
        node2 = TextNode("This is a text node", TextType.ITALIC, "URL")
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


class TestTextNodeSplitDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        new_nodes_expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, new_nodes_expected)

    def test_no_delimiter_returns_same(self):
        node = TextNode("no code here", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [node],
        )

    def test_unmatched_delimiter_raises(self):
        node = TextNode("this `is broken", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_delimited_segments(self):
        node = TextNode("a `b` c `d` e", TextType.TEXT)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.CODE),
            TextNode(" e", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            expected,
        )

    def test_delimiter_at_edges(self):
        node = TextNode("`x`y`z`", TextType.TEXT)
        expected = [
            TextNode("x", TextType.CODE),
            TextNode("y", TextType.TEXT),
            TextNode("z", TextType.CODE),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            expected,
        )

    def test_multi_char_delimiter_bold(self):
        node = TextNode("pre **bold** mid **more** post", TextType.TEXT)
        expected = [
            TextNode("pre ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" mid ", TextType.TEXT),
            TextNode("more", TextType.BOLD),
            TextNode(" post", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            expected,
        )

    def test_single_char_delimiter_italic(self):
        node = TextNode("a _ital_ b", TextType.TEXT)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("ital", TextType.ITALIC),
            TextNode(" b", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            expected,
        )


class TestExttractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )


class TestTextToTextNode(unittest.TestCase):
    def test_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual_nodes = text_to_textnodes(text)

        self.assertEqual(actual_nodes, expected_nodes)


if __name__ == "__main__":
    unittest.main()
