import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq1(self):
        node = TextNode("whatever", TextType.BOLD)
        node2 = TextNode("whatever is clever", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_eq2(self):
        node = TextNode("whatever", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("whatever", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)
    def test_eq3(self):
        node = TextNode("whatever", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("whatever", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()