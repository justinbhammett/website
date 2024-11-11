import re
from textnode import *

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
        
def text_node_to_html_node(textnode):
    match textnode.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=textnode.text, props=None)
        case TextType.BOLD:
            return LeafNode(tag="b", value=textnode.text, props=None)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=textnode.text, props=None)
        case TextType.CODE:
            return LeafNode(tag="code", value=textnode.text, props=None)
        case TextType.LINK:
            return LeafNode(tag="a", value=textnode.text, props={"href": textnode.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": textnode.url, "alt": textnode.text})

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
    output = re.sub(r'\n{3,}', '\n\n', text)
    output = output.split("\n\n")
    new_output = []
    for index, put in enumerate(output):
        if put == "":
            output.pop(index)
        else:
            new_output.append(put.lstrip().rstrip())

    return new_output

def block_to_block_type(text):
    if (text.startswith("# ")
        or text.startswith("## ")
        or text.startswith("### ")
        or text.startswith("#### ")
        or text.startswith("##### ")
        or text.startswith("###### ")):
        return "heading"
    if text.startswith("```") and text.endswith("```"):
        return "code"
    if all(line.startswith(">") for line in text.split("\n")):
        return "quote"
    if all(line.startswith("* ") for line in text.split("\n")):
        return "unordered_list"
    if all(line.startswith("- ") for line in text.split("\n")):
        return "unordered_list"
    if text.startswith("1. "):
        i = 1
        for line in text.split("\n"):
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"

def header_node(text):
    new_text = text.split("\n")
    all_headers = []
  
    
    for nt in new_text:
        nt = nt.strip()  # Remove leading/trailing whitespace
        if not nt.startswith("#"):
            continue  # Skip lines that aren't headers
        
        header_level = 0
        
        # Calculate header level for this line
        while header_level < len(nt) and nt[header_level] == '#':
            header_level += 1
        if header_level > 6:
            header_level = 6
        
        children = t2c(nt[header_level:].strip())  # Strip leading spaces after header level
        
        # Only add if it's indeed a header
        header_node = ParentNode(tag="h"+str(header_level), children=children)
        all_headers.append(header_node)
        # print(all_headers)
    
    return all_headers


# def header_node(block):
#     level = 0
#     for char in block:
#         if char == "#":
#             level += 1
#         else:
#             break
#     if level + 1 >= len(block):
#         raise ValueError(f"Invalid heading level: {level}")
#     text = block[level + 1 :]
#     children = t2c(text)
#     return ParentNode(f"h{level}", children)

def code_node(text):
    children = t2c(text[3:-3])
    child = ParentNode(tag="code",children=children, props=None)
    parent = ParentNode(tag="pre", children=(child,))
    return parent

def quote_node(text):
    new_text = text.split("\n")
    stripped_lines = []
    for line in new_text:
        stripped_lines.append(line[1:].strip())
    children = t2c(" ".join(stripped_lines))
    children = [children] if not isinstance(children, list) else children
    output = ParentNode(tag="blockquote", children=children)
    return output

def unordered_list_node(text):
    new_text = text.split("\n")
    items = []
    for line in new_text:
        stripped_line = line.strip()
        child = t2c(stripped_line[2:])
        items.append(ParentNode("li", child))
    return ParentNode("ul", children=items)

def ordered_list_node(text):
    lines = text.strip().split('\n')
    items = []
    expected_number = 1
    for line in lines:
        stripped_line = line.strip()
        match = re.match(r'^(\d+)', stripped_line)
        ct = len(match.group(1))
        if stripped_line and bool(match) and stripped_line[ct:ct+2] == '. ':
            line_number = int(match.group(1))
            if line_number != expected_number:
                raise Exception("Not numbered correctly")
            child = t2c(stripped_line[ct+2:])
            items.append(ParentNode("li", children=child))
            expected_number += 1
    return ParentNode("ol", children=items)

def paragraph_node(text):
    lines = text.split("\n")
    paragraph = " ".join(lines)
    children = t2c(paragraph)
    return ParentNode("p", children)


def text_to_children(text, block_type):

    if block_type=="heading":
        return header_node(text)

    if block_type=="code":
        return code_node(text)
    
    if block_type=="quote":
        return quote_node(text)
    
    if block_type=="unordered_list":
        return unordered_list_node(text)
    
    if block_type=="ordered_list":
        return ordered_list_node(text)
    
    if block_type=="paragraph":
        return paragraph_node(text)
    


def t2c(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode(tag="div", children=[], props=None)

    for block in blocks:
        block_type = block_to_block_type(block)
        if isinstance(text_to_children(block, block_type),list):
            parent.children.extend(text_to_children(block, block_type))
        else:
            parent.children.append(text_to_children(block, block_type))
        # print(block)
        # print(block_type)
        # print(text_to_children(block, block_type))
        # print(header_node(block))
  
    return parent
        



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
    text9 = "# head1 \n ## **head2** oof\n ### head3"
    # print(split_nodes_link([text6]))
    # split_nodes_image([text5])
    # print(text_to_textnodes(text7))
    # text9 = "####### header 3"
    # print(markdown_to_blocks(text9))
    # text_to_textnodes(text7)
    # print(block_to_block_type(text9))
    # print(markdown_to_html_node(text9))
    # print(t2c(text9))
    # print(block_to_block_type(text9))
    # t2c(text7)
    # print(header_node(text9))

main()



