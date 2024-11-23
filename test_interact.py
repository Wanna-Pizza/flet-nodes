import flet as ft


def main(page: ft.Page):
    lol = ft.TextField('',bgcolor='red')
    page.add(
        ft.InteractiveViewer(
            min_scale=0.1,
            max_scale=15,
            boundary_margin=ft.margin.all(20),
            content=ft.Container(lol,height=1000,width=1000,alignment=ft.alignment.center),
            disabled=True,
        )
    )


ft.app(main)
