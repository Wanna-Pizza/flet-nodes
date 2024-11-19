import flet as ft
import time



def main(page: ft.Page):
    text_str = 'Hello world !!!!!!!!!!!!!!!!!'
    text = ft.Text('',size=60)
    page.add(text)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    for i in text_str:
        text.value = text.value+i
        text.update()
        time.sleep(0.3)






ft.app(main)