import asyncio
import time
import flet as ft
import flet.canvas as cv
from CurveNode import CurveNode

from flet import LayoutBuilder
class PointConnectOutput(ft.Draggable):
    def __init__(self,id=0):
        super().__init__(content = ft.Container(
                    width=20,
                    height=20,
                    shape=ft.BoxShape.CIRCLE,
                    bgcolor='white',
                    ))
        self.id_ = id
        self.group = 'start'
        self._offset_ = 0.0
    
    def calculate_self_position(self):
        top=self.node.top
        height=self.node.height
        circle_size=20
        bar_height=30
        circle_count=len(self.node.outputs)
       
        if circle_count == 0:
            return []
        
        available_height = height - 2 * bar_height - circle_count * circle_size

        if available_height < 0:
            raise ValueError("Not enough space to fit the circles")

        spacing = available_height / (circle_count + 1)
        
        pos = top + bar_height + spacing * (self.id_ + 1) + circle_size * self.id_ + circle_size / 2
        self._offset_ = pos - top
    
    def update_offsets(self):
        self.calculate_self_position()
        self.node.offsets_out.append(self._offset_)

    def did_mount(self):
        self.node = self.parent.parent.parent.parent
        self.node : Node
        self.update_offsets()
        return super().did_mount()

class PointConnectInput(ft.Row):
    def __init__(self,text='None',id=0):
        super().__init__()
        self.text = text
        self.id_ = id
        self.node = None
        self._offset_ = 0.0
        self.controls = self.gen_controls()
    
    def gen_controls(self):
        self.builder = ft.Container(
                    width=20,
                    height=20,
                    shape=ft.BoxShape.CIRCLE,
                    bgcolor=ft.colors.GREY,
                    shadow=ft.BoxShadow(spread_radius=2,blur_radius=0,color=ft.colors.GREY_800)
                    )
        self.drag=ft.DragTarget(
                    on_accept=self.accept,
                    group='start',
                    content=self.builder
                    )
        text = ft.Text(self.text)
        return [self.drag,text]

    def calculate_self_position(self):
        top=self.node.top
        height=self.node.height
        circle_size=20
        bar_height=30
        circle_count=len(self.node.inputs)
       
        if circle_count == 0:
            return []
        
        available_height = height - 2 * bar_height - circle_count * circle_size

        if available_height < 0:
            raise ValueError("Not enough space to fit the circles")

        spacing = available_height / (circle_count + 1)
        
        pos = top + bar_height + spacing * (self.id_ + 1) + circle_size * self.id_ + circle_size / 2
        self._offset_ = pos - top
        print(self._offset_)


        
    def accept(self, e: ft.DragTargetAcceptEvent):
        control = self.page.get_control(e.src_id)
        control: PointConnectOutput

        self.stack: ft.Stack
        left = self.node.left


        curve = CurveNode(
        start=[
            control.node.left+control.node.width,
            control._offset_+control.node.top
        ],
        end=[
            left,
            self._offset_+self.node.top
        ],
                    node_in=control.node,
                    node_out=self.node,
                    id_out=self.id_,
                    id_in=control.id_
                    )

        self.stack.controls.append(
            curve
        )
        self.node.curves.append([curve,'in'])
        control.node.curves.append([curve,'out'])
        self.stack.update()

    def update_offsets(self):
        self.calculate_self_position()
        self.node.offsets_in.append(self._offset_)
    
    def did_mount(self):
        self.node = self.parent.parent.parent
        self.node : Node
        self.stack = self.node.stack
        print(F'ID INPUT: {self.id_}')
        self.update_offsets()
        
        return super().did_mount()


class Node(ft.GestureDetector):
    _id = 1
    def __init__(self, top=0, left=0,on_update=None):
        super().__init__()
        self.id = Node._id 
        Node._id += 1
        self.point_w = 20

        self.curves = []
        self.offsets_in = []
        self.offsets_out = []

        self.text_label = f"Stack {self.id}"
        self.stack = None
        self.on_update = on_update
       
        self.width = 100*4
        self.height = 50*4
        self.top = top
        self.left = left
        self.label = ft.Text(self.text_label)

        self.content = ft.Stack([
            ft.Container(
                self.gen_block()
                
                ,padding=ft.padding.only(left=10,right=10,top=0,bottom=0)),
            self.gen_inputs(),
            
            self.gen_outputs()
            
            ])
        self.on_vertical_drag_update = self.drag_update
        self.on_horizontal_drag_update = self.drag_update
        
        # self.drag_interval = 25
    def gen_block(self):
        self.block_draw = ft.Container(
            width=self.width,
            height=self.height,
                        bgcolor = ft.colors.GREY_900,
                        border = ft.border.all(width=2, color=ft.colors.GREY_800),
                        border_radius = 5,
                        alignment=ft.alignment.center,
                        content = ft.Column([
                            ft.Container(height=30,bgcolor='black,0.4',content=self.label,alignment=ft.alignment.center)
                        ])
                        )
        return self.block_draw
    def gen_inputs(self):

        self.inputs = ['Controls','Expand','Aligment','lol']
        self.in_links = []
        column = ft.Column(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,spacing=0)
        column.controls.append(ft.Container(height=30))
        for index,i in enumerate(self.inputs):
            link = PointConnectInput(text=i,id=index)
            column.controls.append(
                link
            )
            self.in_links.append(link)
        column.controls.append(ft.Container(height=30))
        return column
    
    
    def gen_outputs(self):
        self.outputs = ['Stack','lol','yes']
        self.out_links = []

        column = ft.Column(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,spacing=0)
        column.controls.append(ft.Container(height=30,bgcolor='red'))
        for index,i in enumerate(self.outputs):
            link = PointConnectOutput(id=index)
            column.controls.append(
                link
            )
            self.out_links.append(link)
        column.controls.append(ft.Container(height=30))
        return ft.Row([column],alignment=ft.MainAxisAlignment.END)

    def update_links(self):
        self.offsets_in.clear()
        for i in self.in_links:
            i.update_offsets()
        self.offsets_out.clear()
        for i in self.out_links:
            i.update_offsets()
        
    def update_block_drawer(self,scale_factor):
        self.width *= scale_factor
        self.height *= scale_factor
        self.top *= scale_factor
        self.left *= scale_factor
        self.block_draw.width = self.width
        self.block_draw.height = self.height
        # self.update_links()
        self.page.run_task(self.async_update_curves)
        self.update()
        

    async def async_update_curves(self):
        await asyncio.gather(*(
            self.update_curve(curve, pos) for curve, pos in self.curves
        ))
    

    async def update_curve(self, curve, pos):
        if pos == 'in':
            curve.update_curve_end(y=(self.offsets_in[curve.id_output])+self.top,x=self.left)
        else:
            curve.update_curve_top(y=(self.offsets_out[curve.id_input])+self.top,x=self.left+self.width)


    async def update_ui(self, e):
        new_left = self.left + e.delta_x
        new_top = self.top + e.delta_y
        self.left = new_left
        self.top = new_top

        await asyncio.gather(*(
            self.update_curve(curve, pos) for curve, pos in self.curves
        ))

        self.update()

    def drag_update(self, e: ft.DragUpdateEvent):
        self.page.run_task(self.update_ui,e)
    
    def did_mount(self):
        self.stack = self.parent
        self.connections = self.parent.parent.parent.parent.parent.connections
        return super().did_mount()
    
    

class view_node(ft.Container):
    def __init__(self):
        super().__init__()
        self.connections = []
        self.content = ft.InteractiveViewer(
            content=self._content(),
            # interaction_end_friction_coefficient=0.01,
            boundary_margin=1000,
            constrained=True,
            min_scale=0.01,
            max_scale=10,
            scale_factor=1000,
            # scale_enabled=False,
            width=100000,
            height=100000,
        )
        self.scale = None
        self.border = ft.border.all(2,'red')        
    def add(self,e):
        self.content.width = self.content.width+500
        self.content.update()
    def _content(self):
        self.view = ft.Container(border=ft.border.all(width=3,color='white,0.3'),scale=1,bgcolor='red')
        self.stack_control = ft.Stack([],scale=1)
        self.nodes()

        self.view.content = self.stack_control

        self.ges = ft.GestureDetector(
            content=self.view,
            # on_vertical_drag_update=self.vert_update,
            # on_scroll=self.zoom,
            on_hover=self.hover
            
            )
        return self.ges
    def hover(self,e:ft.HoverEvent):
        self.hover_x = e.local_x
        self.hover_y = e.local_y
    
    async def zoom_async(self, e: ft.ScrollEvent):
        self.zoom_factor = 0.1
        delta = e.scroll_delta_y
        if delta > 0:
            self.scale += self.zoom_factor
        else:
            self.scale -= self.zoom_factor

        self.scale = max(0.1, min(10.0, self.scale))  # Минимум 0.1, максимум 5.0

        self.update()
    def zoom(self,e):
        self.page.run_task(self.zoom_async,e)

    def nodes(self):
        for i in range(30):
            node1 = Node(top=i*500, left=500)
            self.stack_control.controls.append(node1)
        
      


        

class MainView(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = view_node()



def main(page: ft.Page):
    page.update()
    page.add(MainView())
    


ft.app(main,assets_dir="client/fdassets")