import unittest

from htmlnode import *
from textnode import *


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

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(tag="p", value="what?", props={"href": "http://www.google.com"})
        node2 = LeafNode(tag="p", value="what?", props={"href": "http://www.google.com"})
        self.assertEqual(node, node2)
    def test_eq1(self):
        node = LeafNode(tag="hr", value=None, props=None)
        node2 = LeafNode(tag=None, value=None, props=None)
        self.assertNotEqual(node, node2)
    def test_eq2(self):
        node = LeafNode(tag=None, value=None, props=None)
        node2 = LeafNode(tag=None, value=None,  props=None)
        self.assertEqual(node, node2)
    def test_eq3(self):
        node = LeafNode(tag=None, value="What?", props=None)
        node2 = LeafNode(tag=None, value=None, props=None)
        self.assertNotEqual(node, node2)

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(tag="a", children=[LeafNode(tag="p", value="what?"), LeafNode(tag="i", value="italic text")], props={"href": "http://www.google.com"})
        node2 = ParentNode(tag="a", children=[LeafNode(tag="p", value="what?"), LeafNode(tag="i", value="italic text")], props={"href": "http://www.google.com"})
        self.assertEqual(node, node2)
    def test_eq1(self):
        node = ParentNode(tag="p", children=[ParentNode(tag="a", children=[LeafNode(tag="p", value="what?"), LeafNode(tag="i", value="italic text")], props={"href": "http://www.google.com"})], props=None)
        node2 = ParentNode(tag="p", children=[ParentNode(tag="a", children=[LeafNode(tag="p", value="what?"), LeafNode(tag="i", value="italic text")], props={"href": "http://www.google.com"})], props=None)
        self.assertEqual(node, node2)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        textnode1 = TextNode(text="picture of elephant", text_type=TextType.LINK, url="http://www.elephant.com")
        textnode2 = TextNode(text="picture of elephant", text_type=TextType.LINK, url="http://www.elephant.com")
        self.assertEqual(textnode1, textnode2)

if __name__ == "__main__":
    unittest.main()