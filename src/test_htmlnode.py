import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p", value="what?", children=None, props=None)
        node2 = HTMLNode(tag="p", value="what?", children=None, props=None)
        self.assertEqual(node, node2)
    def test_eq1(self):
        node = HTMLNode(tag="hr", value=None, children=None, props=None)
        node2 = HTMLNode(tag=None, value=None, children=None, props=None)
        self.assertNotEqual(node, node2)
    def test_eq2(self):
        node = HTMLNode(tag=None, value=None, children=None, props=None)
        node2 = HTMLNode(tag=None, value=None, children=None, props=None)
        self.assertEqual(node, node2)
    def test_eq3(self):
        node = HTMLNode(tag=None, value="What?", children=None, props=None)
        node2 = HTMLNode(tag=None, value=None, children=None, props=None)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()