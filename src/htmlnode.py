
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
    
def main():
    text1 = HTMLNode(tag="p", value=None, children=None, props={"href": "http://www.google.com", "target": "_blank"})
    print(text1.props_to_html())

main()



