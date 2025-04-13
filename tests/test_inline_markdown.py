import unittest

from src.inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
)
from src.textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_code_multiword(self):
        node = TextNode("This is text with a `code block` and `another`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.CODE),
            ],
            new_nodes,
        )

    def test_delim_invalid(self):
        node = TextNode("This is text with a **bolded word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delim_consecutive_delimiters(self):
        node = TextNode(
            "This is text with **bolded** and **another bolded** word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_invalid(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://example.com)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_invalid(self):
        matches = extract_markdown_images("This text does not contain an image.")
        self.assertListEqual([], matches)

    def test_extract_markdown_multi_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/another.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image", "https://i.imgur.com/another.png"),
            ],
            matches,
        )

    def test_extract_markdown_multi_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com) and another [link](https://example2.com)"
        )
        self.assertListEqual(
            [
                ("link", "https://example.com"),
                ("link", "https://example2.com"),
            ],
            matches,
        )


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode("This is a [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_single(self):
        node = TextNode("[link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_multiple(self):
        node = TextNode(
            "This is a [link](https://example.com) and another [link](https://example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example2.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_multiple_ends_with_text(self):
        node = TextNode(
            "This is a [link](https://example.com) and another [link](https://example2.com) with text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example2.com"),
                TextNode(" with text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is a text without links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link_invalid(self):
        node = TextNode(
            "This is a text with an ![image](https://example.com)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestTextToNodes(unittest.TestCase):
    def text_text_to_text_nodes(self):
        text = "This is a test"
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_text_nodes_empty(self):
        text = ""
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 0)
        self.assertEqual(nodes, [])

    def test_text_to_text_nodes_special_characters(self):
        text = "This is a test with special characters: !@#$%^&*()"
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_text_nodes_bold(self):
        text = "This is a test with **bold** text"
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a test with ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_text_nodes_italic(self):
        text = "This is a test with _italic_ text"
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a test with ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_text_nodes_code(self):
        text = "This is a test with `code` text"
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a test with ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_text_nodes_link(self):
        text = "This is a test with [link](https://example.com) text"
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a test with ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_text_nodes_image(self):
        text = "This is a test with ![image](https://example.com/image.png) text"
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a test with ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/image.png")
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_text_nodes_multiple(self):
        text = (
            "This is a test with **bold** text, _italic_ text, `code` text, "
            "[link](https://example.com) text, and ![image](https://example.com/image.png) text"
        )
        nodes = text_to_text_nodes(text)
        self.assertEqual(len(nodes), 11)
        self.assertEqual(nodes[0].text, "This is a test with ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text, ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " text, ")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " text, ")
        self.assertEqual(nodes[6].text_type, TextType.TEXT)
        self.assertEqual(nodes[7].text, "link")
        self.assertEqual(nodes[7].text_type, TextType.LINK)
        self.assertEqual(nodes[7].url, "https://example.com")
        self.assertEqual(nodes[8].text, " text, and ")
        self.assertEqual(nodes[8].text_type, TextType.TEXT)
        self.assertEqual(nodes[9].text, "image")
        self.assertEqual(nodes[9].text_type, TextType.IMAGE)
        self.assertEqual(nodes[9].url, "https://example.com/image.png")
        self.assertEqual(nodes[10].text, " text")
        self.assertEqual(nodes[10].text_type, TextType.TEXT)
