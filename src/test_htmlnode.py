import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_initialization(self):
        node = HTMLNode("div", {"class": "container"}, "Hello, World!")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, {"class": "container"})
        self.assertEqual(node.children, "Hello, World!")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_value(self):
        node = LeafNode("p", None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_prop(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_missing_tag_raises(self):
        child = LeafNode(None, "text")
        with self.assertRaisesRegex(ValueError, "ParentNode tag cannot be None"):
            ParentNode(None, [child]).to_html()

    def test_children_none_raises_different_message(self):
        # children is explicitly None → different error than missing tag
        with self.assertRaisesRegex(ValueError, "ParentNode children cannot be None"):
            ParentNode("div", None).to_html()

    def test_empty_children_okay_renders_empty_tag(self):
        # Empty list is not "missing" — should render empty container.
        self.assertEqual(ParentNode("div", []).to_html(), "<div></div>")

    def test_multiple_children_mixed_text_and_tags(self):
        kids = [
            LeafNode("b", "Bold"),
            LeafNode(None, " plain "),
            LeafNode("i", "italic"),
            LeafNode(None, "!"),
        ]
        self.assertEqual(
            ParentNode("p", kids).to_html(),
            "<p><b>Bold</b> plain <i>italic</i>!</p>",
        )

    def test_parent_with_props(self):
        kids = [LeafNode(None, "hello")]
        node = ParentNode("div", kids, {"class": "box", "data-x": "1"})
        # Expect quoted attributes; order can matter if you don't sort props.
        html = node.to_html()
        self.assertTrue(html.startswith("<div "))
        self.assertIn('class="box"', html)
        self.assertIn('data-x="1"', html)
        self.assertTrue(html.endswith(">hello</div>"))

    def test_child_with_props(self):
        link = LeafNode("a", "Click", {"href": "https://example.com"})
        node = ParentNode("p", [LeafNode(None, "See "), link])
        self.assertEqual(
            node.to_html(),
            '<p>See <a href="https://example.com">Click</a></p>',
        )

    def test_nested_parents_three_levels_many_children(self):
        inner = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "one")]),
                ParentNode("li", [LeafNode(None, "two")]),
                ParentNode("li", [LeafNode(None, "three")]),
            ],
        )
        outer = ParentNode("div", [LeafNode("h3", "List"), inner])
        self.assertEqual(
            outer.to_html(),
            "<div><h3>List</h3><ul><li>one</li><li>two</li><li>three</li></ul></div>",
        )

    def test_child_leaf_missing_value_bubbles_error(self):
        # If a child LeafNode can't render, ParentNode.to_html should surface the error.
        bad = LeafNode("span", None)
        node = ParentNode("div", [bad])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_non_leaf_child_is_htmlnode_like(self):
        # Parent inside Parent, sibling leaves after
        sub = ParentNode("span", [LeafNode("b", "bold")])
        parent = ParentNode("div", [sub, LeafNode(None, " tail")])
        self.assertEqual(parent.to_html(), "<div><span><b>bold</b></span> tail</div>")

    def test_large_flat_children(self):
        kids = [LeafNode("span", f"#{i}") for i in range(5)]
        node = ParentNode("p", kids)
        self.assertEqual(
            node.to_html(),
            "<p><span>#0</span><span>#1</span><span>#2</span><span>#3</span><span>#4</span></p>",
        )

    def test_text_only_children(self):
        node = ParentNode(
            "p", [LeafNode(None, "A"), LeafNode(None, "B"), LeafNode(None, "C")]
        )
        self.assertEqual(node.to_html(), "<p>ABC</p>")

    def test_empty_text_child(self):
        # Empty string should render as nothing, not error
        node = ParentNode("p", [LeafNode(None, ""), LeafNode("em", "x")])
        self.assertEqual(node.to_html(), "<p><em>x</em></p>")


if __name__ == "__main__":
    unittest.main()
