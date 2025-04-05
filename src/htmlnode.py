class HTMLNode:
    """
    A class representing a node in an HTML document.
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Initialize an HTMLNode with optional tag, value, children, and props.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html() must be implemented in subclasses")

    def props_to_html(self):
        """
        Convert the props dictionary to an HTML attribute string.
        """
        if not self.props:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        """
        Return a string representation of the HTMLNode.
        """
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    """
    A LeafNode represents a single HTML element with a tag and value.
    """

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("invalid HTML: no value")
        return (
            f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            if self.tag
            else self.value
        )

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HTMLNode):
    """
    A ParentNode represents an HTML element that can have children.
    """

    def __init__(self, tag, children: list[LeafNode], props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("invalid HTML: no tag")
        if not self.children:
            raise ValueError("invalid HTML: no children")
        return (
            f"<{self.tag}{self.props_to_html()}>"
            + "".join(child.to_html() for child in self.children)
            + f"</{self.tag}>"
        )

    def __repr__(self):
        return (
            f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
        )
