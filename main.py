import asyncio
import time
import flet as ft
import flet.canvas as cv
from CurveNode import CurveNode

class PointConnectOutput(ft.Draggable):
    def __init__(self,name=''):
        super().__init__(content = ft.Container(
                    width=20,
                    height=20,
                    shape=ft.BoxShape.CIRCLE,
                    bgcolor='white',
                    border=ft.border.all(width=3,color=ft.Colors.GREY_800)
                    ))
        
        self.name = name
        self.id_node = None
        self.group = 'start'

    def did_mount(self):
        node_data = self.parent.parent.parent.parent
        print(node_data.id)
        self.id_node = node_data.id
        return super().did_mount()
class PointConnectInput(ft.DragTarget):
    def __init__(self,name=''):
        super().__init__(content=ft.Container(
                    width=20,
                    height=20,
                    shape=ft.BoxShape.CIRCLE,
                    bgcolor='red',
                    border=ft.border.all(width=3,color=ft.Colors.GREY_800)
                    ))
        self.name = name
        self.id_node = None
        self.group='start'
        self.on_accept=self.accept
    
    
    
    def accept(self,e:ft.DragTargetAcceptEvent):
        src = self.page.get_control(e.src_id)
        print(src.name)
        print(src.node_data)
    
    def did_mount(self):
        node_data = self.parent.parent.parent.parent
        print(node_data.id)
        self.id_node = node_data.id
        return super().did_mount()


class Node(ft.GestureDetector):
    _id = 1
    def __init__(self, top=0, left=0,on_update=None,on_drag_point=None):
        super().__init__()
        self.id = Node._id 
        Node._id += 1

        self.on_update = on_update
        self.point_connect_in = PointConnectInput(name='stack')
        self.point_connect_out = PointConnectOutput(name='stack')
        
       
        self.width = 100*4
        self.height = 50*4
        self.top = top
        self.left = left
        self.text_label = f"Stack {self.id}"
        self.label = ft.Text(self.text_label)
        self.block_draw = ft.Container(
                        left=10,
                        height=self.height,
                        width=self.width-20,
                        bgcolor = ft.colors.GREY_900,
                        border = ft.border.all(width=2, color=ft.Colors.GREY_800),
                        border_radius = 5,
                        alignment=ft.alignment.center,
                        content = self.label
                        )
        self.content = ft.Stack([
            self.block_draw,
            #inputs
            ft.Column([ft.Row([self.point_connect_in],alignment=ft.MainAxisAlignment.START)],alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Column([ft.Row([self.point_connect_out],alignment=ft.MainAxisAlignment.END)],alignment=ft.MainAxisAlignment.CENTER)
                                
            
            ])
        self.on_vertical_drag_update = self.drag_update
    def update_block_drawer(self):
        self.block_draw.width = self.width-20
        self.block_draw.height = self.height
       

    def drag_update(self, e: ft.DragUpdateEvent):
        self.top += e.delta_y
        self.left += e.delta_x
        self.update()
        if self.on_update:
            self.on_update(self.top,self.left,self.height,self.width)


class view_node(ft.Stack):
    def __init__(self):
        super().__init__()
        self.hover_x = 0
        self.hover_y = 0
        self.connection = []
        self.nodes()
        self.controls = [self._content()]
    
    async def update_node(self,node, scale_factor):
        try:
            node.width *= scale_factor
            node.height *= scale_factor
            node.top *= scale_factor
            node.left *= scale_factor
            node.update_block_drawer()
            node.on_update(node.top, node.left, node.height, node.width)
            node.update()
        except Exception as e:
            pass

    
    def vert_start(self,e: ft.DragStartEvent):
        pass


    def vert_update(self, e: ft.DragUpdateEvent):
        self.ges.top = self.ges.top + e.delta_y
        self.ges.left = self.ges.left + e.delta_x
        self.update()
    
    def move(self,y,x):
        self.ges.top = y
        self.ges.left = x
        self.ges.update()

    async def zoom_async(self, e: ft.ScrollEvent):
        scale_step = 50*self.view.width/1000
        prev_width = self.view.width
        prev_height = self.view.height

        if e.scroll_delta_y < 0:
            self.view.width += scale_step
            self.view.height += scale_step
        elif e.scroll_delta_y > 0:
            self.view.width = max(50, self.view.width - scale_step)
            self.view.height = max(50, self.view.height - scale_step)

        dx = (self.hover_x / prev_width) * scale_step
        dy = (self.hover_y / prev_height) * scale_step

        if e.scroll_delta_y < 0:
            self.ges.left -= dx
            self.ges.top -= dy
        elif e.scroll_delta_y > 0:
            self.ges.left += dx
            self.ges.top += dy

        scale_factor = self.view.width / prev_width

        update_tasks = []
        for node in self.stack_control.controls:
            task = asyncio.create_task(self.update_node(node, scale_factor))
            update_tasks.append(task)

        await asyncio.gather(*update_tasks)

        self.update()
        
    def hover(self,e:ft.HoverEvent):
        self.hover_x = e.local_x
        self.hover_y = e.local_y
    
    def zoom(self,e):
        self.page.run_task(self.zoom_async,e)


    def _content(self):
        self.view = ft.Container(border=ft.border.all(width=3,color='white,0.3'),width=4000,height=4000)
        self.stack_control = ft.Stack([self.node1,self.node2])
        self.view.content = self.stack_control
        self.ges = ft.GestureDetector(
            content=self.view,
            on_vertical_drag_start=self.vert_start,
            on_vertical_drag_update=self.vert_update,
            top=0,left=0,
            on_scroll=self.zoom,
            on_hover=self.hover
            
            )
        
        return self.ges

    def add_node(self,e: ft.DragUpdateEvent):
        self.stack_control.controls.append(Node(
            top=e.global_y,
            left=e.global_x,
            on_drag_point=self.add_node))
        self.stack_control.update()

    def nodes(self):
        def start_update(top,left,height,width):
            [left+100,top+25]
            self.curve.update_curve_top([top+height/2,left+width])

        def end_update(top,left,height,width):
            self.curve.update_curve_end([top+height/2,left])
        


        self.node1 = Node(top=100, left=100)
        self.node2 = Node(top=150, left=800)
        # self.curve = CurveNode(start=[100+25,100+100],end=[175,300])

class MainView(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = ft.Row([ft.Container(width=200,border=ft.border.all(width=2,color='white,0.2'),border_radius=10),ft.Container(view_node(),expand=True)])
        self.expand = True
        # self.content = ft.Container(width=100,height=100,bgcolor='red')



def main(page: ft.Page):
    page.update()
    page.add(MainView())
    


ft.app(main,assets_dir="client/fdassets")