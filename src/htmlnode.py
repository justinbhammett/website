from textnode import *

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props

    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        output_string = ""
        for prop in self.props:
            output_string += (" " + prop + "=\"" + self.props[prop] + "\"")
        return (f"{output_string}")
    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return (self.tag == other.tag and
                    self.value == other.value and
                    self.children == other.children and
                    self.props == other.props)
        return False
    def __repr__(self):
        return f"{' '.join(f'{key}={value}' for key, value in self.__dict__.items())}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value is None:
            raise ValueError("no value")
        if self.tag is None:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        # prop_iteration = f"{' '.join(f'{key}="{value}"' for key, value in self.props.items())}"
        prop_iteration = self.props_to_html()
        return f"<{self.tag} {prop_iteration}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children, props=None)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag")
        if self.children is None:
            raise ValueError("no children")
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        child_iteration = f"{' '.join(f'{kid.to_html()}' for kid in self.children)}"
        # prop_iteration = f"{' '.join(f'{key}="{value}"' for key, value in self.props.items())}"
        prop_iteration = self.props_to_html()
        return f"<{self.tag} {prop_iteration}>{child_iteration}</{self.tag}>"
   
    def __repr__(self):
            return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
        
def text_node_to_html_node(TextNode):
    match TextNode.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=TextNode.text, props=None)
        case TextType.BOLD:
            return LeafNode(tag="b", value=TextNode.text, props=None)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=TextNode.text, props=None)
        case TextType.CODE:
            return LeafNode(tag="code", value=TextNode.text, props=None)
        case TextType.LINK:
            return LeafNode(tag="a", value=TextNode.text, props={"href": TextNode.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": TextNode.url, "alt": TextNode.text})

    raise Exception("Invalid type")
        



def main():
    text1 = HTMLNode(tag="p", value=None, children=None, props={"href": "http://www.google.com", "target": "_blank"})
    # print(text1.props_to_html())

    leaf1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    # print(leaf1.to_html())

    parent1 = ParentNode("a", [LeafNode("p", "Click me!"), LeafNode("p", "Don't do it!")], {"href": "https://www.amazon.com"})
    # print(parent1.to_html())

    text2 = TextNode("What is this?", TextType.BOLD, "https://www.boot.dev")
    print(text_node_to_html_node(text2).to_html())

main()



