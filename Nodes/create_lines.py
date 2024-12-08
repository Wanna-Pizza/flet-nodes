def format_code(code):
    lines = code.split('\n')  # Разделяем код на строки
    indented_code = []
    indent_level = 0

    for line in lines:
        stripped_line = line.strip()  # Убираем начальные и конечные пробелы

        if stripped_line.endswith(':'):
            # Если строка заканчивается на двоеточие, это начало нового блока, увеличиваем отступ
            indented_code.append('    ' * indent_level + stripped_line)
            indent_level += 1
        elif stripped_line.endswith('('):
            indented_code.append('    ' * indent_level + stripped_line)
            indent_level += 1
        elif stripped_line.endswith('['):
            indented_code.append('    ' * indent_level + stripped_line)
            indent_level += 1
        
        elif stripped_line == '':
            indented_code.append('')
        else:
            indented_code.append('    ' * indent_level + stripped_line)

            if stripped_line.startswith('return') or stripped_line.startswith('else') or stripped_line.startswith('except'):
                indent_level = max(indent_level - 1, 0)

    return '\n'.join(indented_code)

# Пример кода без отступов
code = """
class app:
    def __init__(self,page: ft.Page):
        super().__init__()
        page.add(ft.Stack(
    controls=[
    ft.Container(content=ft.Row(controls=[
    ft.Text(value="Lol",size=20),
    ft.Text(value="Lol_again",size=20)
])),
    ft.Text(value="Lol",size=20),
    ft.Text(value="Lol_again",size=20)
]))

ft.app(app)
"""

formatted_code = format_code(code)
print(formatted_code)
