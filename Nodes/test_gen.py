def __row(controls):
    controls_str = ',\n    '.join(controls)
    return f'''ft.Row(controls=[\n    {controls_str}\n])'''

def __container(content):
    return f'ft.Container(content={content})'

def __text(value, size):
    value = value.replace("'", '"')
    return f'ft.Text(value="{value}",size={size})'


def __stack(controls):
    controls_str = ',\n    '.join(controls)
    return f'''ft.Stack(
    controls=[\n    {controls_str}\n])'''


def __init_app(content):
    return f'''
class app:
    def __init__(self,page: ft.Page):
        super().__init__()
        page.add({content})

ft.app(app)
'''




text = __text('Lol', size=20)
text1 = __text('Lol_again', size=20)

command1 = __row([text, text1])

command2 = __container(command1)

command3 = __stack([command2,text,text1])


command4 = __init_app(command3)
print(command4.replace("'",''))


import flet as ft


