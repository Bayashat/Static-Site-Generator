import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("p", "This is a paragraph", [], {"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "text"})

    def test_add_child(self):
        childs = [
            HTMLNode("p", "Child 1"),
            HTMLNode("p", "Child 2"),
        ]
        node = HTMLNode("div", "Parent", childs)
        self.assertEqual(node.children, childs)
        self.assertEqual(node.value, "Parent")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("a", "Link", [], {"href": "https://example.com"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=a, value=Link, children=[], props={'href': 'https://example.com'})",
        )

        node = HTMLNode("div", "Container")
        self.assertEqual(
            repr(node), "HTMLNode(tag=div, value=Container, children=None, props=None)"
        )

    def test_props_to_html(self):
        node = HTMLNode("img", None, [], {"src": "image.png", "alt": "An image"})
        self.assertEqual(node.props_to_html(), ' src="image.png" alt="An image"')

        node = HTMLNode(
            "input", None, [], {"type": "text", "placeholder": "Enter text"}
        )
        self.assertEqual(node.props_to_html(), ' type="text" placeholder="Enter text"')

    def test_to_html(self):
        node = HTMLNode("p", "This is a paragraph", [], {"class": "text"})
        self.assertRaises(NotImplementedError, node.to_html)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_leaf_to_html_without_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_without_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_without_props(self):
        node = LeafNode("span", "Hello")
        self.assertEqual(node.to_html(), "<span>Hello</span>")

    def test_leaf_to_html_with_empty_props(self):
        node = LeafNode("span", "Hello", {})
        self.assertEqual(node.to_html(), "<span>Hello</span>")


class TestParentNode(unittest.TestCase):
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

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span><span>child2</span></div>",
        )

    def test_to_html_without_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_without_children(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_repr(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            repr(parent_node),
            "ParentNode(tag=div, children=[LeafNode(tag=span, value=child, props=None)], props=None)",
        )
