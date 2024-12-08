from Node import Node
import flet as ft

class TextNode(Node):
    def __init__(self, top=0, left=0, on_update=None, label="Text"):
        inputs = ["Value", "Size"]
        outputs = ["Text"] 
        super().__init__(top, left, on_update, label, inputs, outputs)
        self.value = 'TextLol'
        self.size = 20
        self.command = f'ft.Text(value={self.value},size={self.size})'

class ValueInput(Node):
    def __init__(self, top=0, left=0, on_update=None, label="Value"):
        inputs = []
        outputs = ["Value"] 
        text_field = ft.TextField(value='0.3',text_size=20)

        super().__init__(top, left, on_update, label, inputs, outputs,content_block=text_field,height=150)
        self.value = 'Fuck yeah'
        self.size = 20
        self.command = f'ft.Text(value={self.value},size={self.size})'
        self.text_field = text_field
        self.init_field()
        
    def init_field(self):
        self.text_field.value = self.value

