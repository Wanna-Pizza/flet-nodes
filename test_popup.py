import asyncio
import time
import flet as ft

class button_item(ft.Row):
    def __init__(self,name:str = 'Button', icon:str = ft.icons.CAMERA_ALT_OUTLINED,on_click=None):
        super().__init__()
        self._on_click = on_click
        self._name = name
        self._icon = icon
        self.controls = self.button_item()
        self.spacing = 30
        self.alignment = ft.MainAxisAlignment.END
        self.offset = [1,0]
        self.animate_offset = ft.Animation(duration=300,curve=ft.AnimationCurve.FAST_OUT_SLOWIN)
    
    async def animate_on(self):
        self.offset = [0,0]
        self.update()

    async def animate_off(self):
        self.offset = [1,0]
        self.update()
    def on_click(self,e):
        if self._on_click:
            self._on_click(self._name)
        


    def button_item(self):
        def on_hover(e):
            circle_button.scale = 1 if circle_button.scale!=1 else 1.1
            circle_button.update()
        text = ft.Text(self._name,size=25)
        icon = ft.Icon(self._icon,size=40,color='black,0.8')

        circle_button = ft.Container(
            width=100,height=100,
            alignment=ft.alignment.center,
            bgcolor='white',
            shape=ft.BoxShape.CIRCLE,on_click=self.on_click,
            scale=1,
            animate_scale=ft.Animation(duration=200,curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT),
            on_hover=on_hover)
        
        circle_button.shadow = ft.BoxShadow(spread_radius=0,blur_radius=20,offset=[4,4],color='black,0.5')
        circle_button.content = icon

        return [text,circle_button]



class main_b(ft.Container):
    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = self.width
        self.border_radius = self.width/2
        self.bgcolor = 'green'
        self.on_tap_down = self.open_menu
        self.content = ft.Icon(ft.icons.EDIT_NOTE,size=50,color='white')
        self.rotate = 0
        self.animate_rotation = ft.Animation(duration=300,curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT)
        
    def close_menu(self,e):
        self.page.run_task(self.animate_closing)
    
    def swith_button(self):
        self.rotate = 3.14/2 if self.rotate!=3.14/2 else 0
        self.content.name = ft.icons.CLOSE if self.content.name!=ft.icons.CLOSE else ft.icons.EDIT_NOTE
        self.update()
    
    def on_click_menu_button(self,e):
        print(e)
    
    def open_menu(self,e:ft.TapEvent):
        self.swith_button()
        x = e.global_x-e.local_x+self.width
        y = e.global_y-e.local_y
        spacing = 30
        width_con = 400
        self.column_menu = ft.Column([
            button_item(on_click=self.on_click_menu_button,name='Camera',icon=ft.icons.CAMERA_ALT_OUTLINED),
            button_item(on_click=self.on_click_menu_button,name='Settings',icon=ft.icons.SETTINGS),
            button_item(on_click=self.on_click_menu_button,name='ASK',icon=ft.icons.QUESTION_ANSWER)],spacing=spacing)
        
        len_controls = len(self.column_menu.controls)
        
        height = (spacing*len_controls)+(100*len_controls)

        con = ft.Container(width=width_con,height=height,top=y-height,left=x-width_con,expand=True,on_click=self.close_menu) # MAIN
        con.content = self.column_menu

        con_full_screen = ft.Container(expand=True,on_click=self.close_menu)
        self.page.overlay.append(con_full_screen)
        
        self.page.overlay.append(con)
        
        self.on_tap_down = self.close_menu
        self.update()
        self.page.update()


        self.page.run_task(self.animate_opening)
    



    async def animate_opening(self):
        await asyncio.sleep(0.03)
        controls = self.column_menu.controls
        controls.reverse()
        for i in controls:
            await i.animate_on()
            await asyncio.sleep(0.05)
    
    async def animate_closing(self):
        self.swith_button()
        for i in self.column_menu.controls:
            await i.animate_off()
            await asyncio.sleep(0.05)
        self.page.overlay.clear()
        self.page.update()
        self.on_tap_down = self.open_menu


    def did_mount(self):

        return super().did_mount()


def main(page: ft.Page):
    page.padding = 40
    page.vertical_alignment = ft.MainAxisAlignment.END
    page.horizontal_alignment = ft.CrossAxisAlignment.END
    page.add(main_b())
ft.app(main)