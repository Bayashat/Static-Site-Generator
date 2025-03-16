from textnode import TextNode, TextType


def main():
    text_nodes = [
        TextNode("Hello", TextType.NORMAL),
        TextNode("This is some anchor text", TextType.LINK, "https://example.com"),
        TextNode("This is some code", TextType.CODE),
        TextNode("This is some bold text", TextType.BOLD),
        TextNode("This is some italic text", TextType.ITALIC),
        TextNode("This is an image", TextType.IMAGE, "https://example.com/image.png"),
    ]
    for node in text_nodes:
        print(node)
        print("-" * 20)


if __name__ == "__main__":
    main()
