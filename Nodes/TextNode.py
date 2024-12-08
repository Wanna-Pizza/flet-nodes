from Node import Node


class TextNode(Node):
    def __init__(self, top=0, left=0, on_update=None, label="Text"):
        inputs = ["Value", "Size"]
        outputs = ["Text"] 
        super().__init__(top, left, on_update, label, inputs, outputs)
        self.value = 'TextLol'
        self.size = 20
        self.command = f'ft.Text(value={self.value},size={self.size})'

