import asyncio
import time
import flet as ft
import flet.canvas as cv
from CurveNode import CurveNode

class PointConnectOutput(ft.Draggable):
    def __init__(self):
        super().__init__(content = ft.Container(
                    width=20,
                    height=20,
                    shape=ft.BoxShape.CIRCLE,
                    bgcolor='white',
                    border=ft.border.all(width=3,color=ft.colors.GREY_800)
                    ))
        
        self.name = None
        self.node_data = None
        self.id_node = None
        self.group = 'start'

    def did_mount(self):
        self.node_data = self.parent.parent.parent.parent
        self.id_node = self.node_data.id
        self.name = self.node_data.text_label

        return super().did_mount()
class PointConnectInput(ft.DragTarget):
    def __init__(self):
        super().__init__(content=ft.Container(
                    width=20,
                    height=20,
                    shape=ft.BoxShape.CIRCLE,
                    bgcolor='red',
                    border=ft.border.all(width=3,color=ft.colors.GREY_800)
                    ))
        self.name = None
        self.id_node:Node = None
        self.node_data = None
        self.stack_nodes:ft.Stack = None
        self.connections: list = None
        self.group='start'
        self.on_accept=self.accept

    
    def accept(self, e: ft.DragTargetAcceptEvent):
        src = self.page.get_control(e.src_id)
        node = src

        end_x = self.node_data.left
        end_y = self.node_data.top+self.node_data.height/2

        start_x = node.node_data.left+node.node_data.width
        start_y = node.node_data.top+node.node_data.height/2
        curve = CurveNode(
                end=[end_x, end_y],
                start=[start_x, start_y],
                node_out=self.node_data,
                node_in=node.node_data
            )
        self.stack_nodes.controls.insert(0,
            curve
        )
        self.stack_nodes.update()
        # self.connections.append(curve)
        self.node_data.curves.append((curve,'out'))
        node.node_data.curves.append((curve,'in'))
        

    
    def did_mount(self):
        self.node_data = self.parent.parent.parent.parent
        self.name = self.node_data.text_label
        self.id_node = self.node_data.id
        self.stack_nodes = self.node_data.stack_nodes
        self.connections = self.node_data.connections

        return super().did_mount()


class Node(ft.GestureDetector):
    _id = 1
    def __init__(self, top=0, left=0,on_update=None,on_drag_point=None):
        super().__init__()
        self.id = Node._id 
        Node._id += 1
        self.point_w = 20

        self.previous_top = 0
        self.previous_left = 0

        self.curves = []

        self.text_label = f"Stack {self.id}"

        self.on_update = on_update
        self.point_connect_in = PointConnectInput()
        self.point_connect_out = PointConnectOutput()
        
       
        self.width = 100*4
        self.height = 50*4
        self.top = top
        self.left = left
        self.label = ft.Text(self.text_label)
        self.block_draw = ft.Container(
                        left=self.point_w/2,
                        height=self.height,
                        width=self.width-self.point_w,
                        bgcolor = ft.colors.GREY_900,
                        border = ft.border.all(width=2, color=ft.colors.GREY_800),
                        border_radius = 5,
                        alignment=ft.alignment.center,
                        content = self.label
                        )
        self.content = ft.Stack([
            self.block_draw,
            ft.Column([ft.Row([self.point_connect_in],alignment=ft.MainAxisAlignment.START)],alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Column([ft.Row([self.point_connect_out],alignment=ft.MainAxisAlignment.END)],alignment=ft.MainAxisAlignment.CENTER)
                                
            
            ])
        self.on_vertical_drag_update = self.drag_update
        self.drag_interval = 25
    def update_block_drawer(self):
        self.block_draw.width = self.width-20
        self.block_draw.height = self.height
    

    async def update_ui(self, e):
        new_left = self.left + e.delta_x
        new_top = self.top + e.delta_y
        self.left = new_left
        self.top = new_top

        await asyncio.gather(*(
            self.update_curve(curve, pos) for curve, pos in self.curves
        ))

        # Применяем изменения
        self.update()



    async def update_curve(self, curve, pos):
        if pos == 'out':
            curve.update_curve_end()
        else:
            curve.update_curve_top()

    def drag_update(self, e: ft.DragUpdateEvent):
        self.page.run_task(self.update_ui,e)

            
    
    def did_mount(self):
        self.stack_nodes = self.parent
        self.connections = self.parent.parent.parent.parent.connections # CONNECTIONS
        return super().did_mount()
class view_node(ft.Stack):
    def __init__(self):
        super().__init__()
        self.hover_x = 0
        self.hover_y = 0
        self.connections = ['LOOL']
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
        self.stack_control = ft.Stack([self.node1,self.node2,self.node3,self.node4])
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
        


        self.node1 = Node(top=100, left=150)
        self.node2 = Node(top=150, left=600)
        self.node3 = Node(top=500, left=600)
        self.node4 = Node(top=800, left=600)

        
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