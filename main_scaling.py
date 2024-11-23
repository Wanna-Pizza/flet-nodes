import asyncio
import time
import flet as ft
import flet.canvas as cv
from CurveNode import CurveNode

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
        self.update_links()
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
        self.connections = self.parent.parent.parent.parent.connections
        return super().did_mount()
    
    

class view_node(ft.Stack):
    def __init__(self):
        super().__init__()
        self.hover_x = 0
        self.hover_y = 0
        self.connections = []
        self.nodes()
        self.scale = 1
        self.controls = [self._content()]
    
    async def update_node(self,node, scale_factor):
        if isinstance(node,Node):
            node.update_block_drawer(scale_factor)
    


    def vert_update(self, e: ft.DragUpdateEvent):
        self.ges.top = self.ges.top + e.delta_y*self.ges.scale
        self.ges.left = self.ges.left + e.delta_x*self.ges.scale
        self.update()
        
    async def zoom_async(self, e: ft.ScrollEvent):
        scale_step = 0.05
        mouse_x, mouse_y = e.global_x, e.global_y
        mouse_l_x, mouse_l_y = e.local_x, e.local_y
        o_left = self.ges.left
        o_top = self.ges.top

        if e.scroll_delta_y < 0:
            self.ges.scale += scale_step

        elif e.scroll_delta_y > 0:
            self.ges.scale -= scale_step


        original_width = self.view.width
        scale = self.ges.scale

        scaled_width = original_width * scale

        difference = original_width - scaled_width

        self.page.overlay.append(ft.Container(
            bgcolor='red',
            height=10,
            width=10,
            top=mouse_y,
            left=mouse_x
        ))
        self.page.update()


        self.update()





        
    def hover(self,e:ft.HoverEvent):
        self.hover_x = e.local_x
        self.hover_y = e.local_y

        self.hover_g_x = e.global_x
        self.hover_g_y = e.global_y
        
    
    def zoom(self,e):
        self.page.run_task(self.zoom_async,e)


    def _content(self):
        self.view = ft.Container(border=ft.border.all(width=3,color='white,0.3'),width=800,height=800)
        self.stack_control = ft.Stack([self.node1,self.node2])
        self.view.content = self.stack_control
        self.ges = ft.GestureDetector(
            content=self.view,
            on_vertical_drag_update=self.vert_update,
            top=0,left=0,
            on_scroll=self.zoom,
            on_hover=self.hover,
            scale=1
            
            )
        
        return self.ges

    def nodes(self):
        self.node1 = Node(top=100, left=500)
        self.node2 = Node(top=350, left=10)
        
      


        

class MainView(ft.Container):
    def __init__(self):
        super().__init__()
        self.content = view_node()
        self.expand = True



def main(page: ft.Page):
    page.update()
    page.add(MainView())
    


ft.app(main,assets_dir="client/fdassets")