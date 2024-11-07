import re
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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i in range(len(sections)):

            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            if i % 2 != 0:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches   

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    start_node = TextNode(text, TextType.TEXT)
    output_nodes = [start_node]
    output_nodes = split_nodes_delimiter(output_nodes, "**", TextType.BOLD)
    output_nodes = split_nodes_delimiter(output_nodes, "*", TextType.ITALIC)
    output_nodes = split_nodes_delimiter(output_nodes, "`", TextType.CODE)
    output_nodes = split_nodes_image(output_nodes)
    output_nodes = split_nodes_link(output_nodes)

    return output_nodes
        
def markdown_to_blocks(text):
    output = text.split("\n\n")
    new_output = []
    for index, put in enumerate(output):
        if put == "":
            output.pop(index)
        else:
            new_output.append(put.lstrip().rstrip())

    return new_output

def block_to_block_type(text):

    if text.startswith("#"):
        header_level = 0 
        while header_level < len(text) and text[header_level] == '#':
            header_level += 1
        if header_level > 6:
            header_level = 6
        return f"<h{header_level}>{text[header_level:]}</h{header_level}>"

    if text.startswith("```") and text.endswith("```"):
        return f"<code>{text[3:-3]} </code>"
    
    if text.startswith(">"):
        new_text = text.split("\n")
        stripped_lines = []
        for line in new_text:
            if line.startswith('>'):
                stripped_lines.append(line[1:].strip())
            else:
                return text
        return f"<q>{"\n".join(stripped_lines)}</q>"
    
    if text.startswith("*") or text.startswith("-"):
        new_text = text.split("\n")
        html_list = ['<ul>']
        for line in new_text:
            stripped_line = line.strip()
            if stripped_line.startswith('- ') or stripped_line.startswith('* '):
                html_list.append(f'<li>{stripped_line[2:]}</li>')
            else:
                return text
        html_list.append('</ul>')
        return '\n'.join(html_list)
    
    if text.startswith("1."):
        lines = text.strip().split('\n')
        html_list = ['<ol>']
        expected_number = 1
        for line in lines:
            stripped_line = line.strip()
            if stripped_line and stripped_line[0].isdigit() and stripped_line[1:3] == '. ':
                line_number = int(stripped_line[0])
                if line_number != expected_number:
                    return text
                html_list.append(f'<li>{stripped_line[3:]}</li>')
                expected_number += 1
            else:
                return text
        html_list.append('</ol>')
        return '\n'.join(html_list)
        



def main():
    text1 = HTMLNode(tag="p", value=None, children=None, props={"href": "http://www.google.com", "target": "_blank"})
    # print(text1.props_to_html())

    leaf1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    # print(leaf1.to_html())

    parent1 = ParentNode("a", [LeafNode("p", "Click me!"), LeafNode("p", "Don't do it!")], {"href": "https://www.amazon.com"})
    # print(parent1.to_html())

    text2 = TextNode("What is this?", TextType.BOLD, "https://www.boot.dev")
    # print(text_node_to_html_node(text2).to_html())

    node2 = TextNode("This is **text** with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node2], "**", TextType.BOLD)
    # print(new_nodes)

    text100 = "some bullshit links ![Adios jose](https://www.boot.dev)"
    # print(extract_markdown_images(text100))
    text10 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # print(extract_markdown_images(text100)[0][1])

    text5 = TextNode("This is text with an image ![alt text](https://www.boots.dev/image.png) actually two images ![another one](https://www.google.com/logo.img) and that's it.", TextType.TEXT,)
    text6 = TextNode("This is text with a link in it [link 1](http://www.google.com)", TextType.TEXT)
    text7 = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    text8 = "     This is a test\n\n\n\n block 2\n\n block 3\n  block 3a  \nblock3b"
    # print(split_nodes_link([text6]))
    # split_nodes_image([text5])
    # print(text_to_textnodes(text7))
    text9 = "####### header 3"
    # markdown_to_blocks(text8)
    # text_to_textnodes(text7)
    print(block_to_block_type(text9))
main()



