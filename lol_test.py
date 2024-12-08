import autopep8

# Исходный код (как строка)
code = """
def example_function(x, y, z):
result = x + y + z
if result > 10:
return 'Greater than 10'
else:
return 'Less or equal to 10'
"""

# Используем autopep8 для форматирования кода
formatted_code = autopep8.fix_code(code, options={'aggressive': 1})

# Выводим результат
if formatted_code != code:
    print("Код был изменен:")
    print(formatted_code)
else:
    print("Код уже отформатирован.")
