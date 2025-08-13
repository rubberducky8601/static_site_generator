class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")

    def props_to_html(self):
        atr = ""
        if not self.props:
            return atr
        for key, value in self.props.items():
            atr += f' {key}="{value}"'
        return atr

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")

        if self.tag is None:
            return self.value

        if self.props is not None:
            props_html = self.props_to_html()
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode tag cannot be None")
        if self.children is None:
            raise ValueError("ParentNode children cannot be None")

        concat = ""
        for child in self.children:
            concat += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{concat}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
