import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(repr(node), "TextNode(This is a text node, text, None)")

    def test_init(self):
        node = TextNode("Another text node", TextType.ITALIC)
        self.assertEqual(node.text, "Another text node")
        self.assertEqual(node.text_type, TextType.ITALIC)
        self.assertIsNone(node.url)

        node_with_url = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node_with_url.text, "Link text")
        self.assertEqual(node_with_url.text_type, TextType.LINK)
        self.assertEqual(node_with_url.url, "https://example.com")

    def test_text_type(self):
        normal_node = TextNode("Normal text", TextType.TEXT)
        bold_node = TextNode("Bold text", TextType.BOLD)
        italic_node = TextNode("Italic text", TextType.ITALIC)

        self.assertEqual(normal_node.text_type, TextType.TEXT)
        self.assertEqual(bold_node.text_type, TextType.BOLD)
        self.assertEqual(italic_node.text_type, TextType.ITALIC)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode(
            "This is a link text node", TextType.LINK, "https://example.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode(
            "This is an image text node",
            TextType.IMAGE,
            "https://example.com/image.png",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://example.com/image.png",
                "alt": "This is an image text node",
            },
        )

    def test_invalid_text_type(self):
        node = TextNode("This is an invalid text type", "invalid_type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
