import flet as ft

from input_output import PointConnectInput,PointConnectOutput

import asyncio


class Node(ft.GestureDetector):
    _id = 1
    def __init__(self, top=0, left=0,on_update=None,label="Stack",inputs=[],outputs=[],content_block=None,height=50*4):
        super().__init__()
        self.id = Node._id 
        Node._id += 1
        self.point_w = 20

        self.curves = []
        self.content_block_ = content_block
        self.inputs = inputs
        self.outputs = outputs
        self.offsets_in = []
        self.offsets_out = []

        self.text_label = f"{label} {self.id}"
        self.stack = None
        self.on_update = on_update
       
        self.width = 100*4
        self.height = height
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
        
    def gen_block(self):
        self.block_draw = ft.Container(
            width=self.width,
            height=self.height,
                        bgcolor = ft.colors.GREY_900,
                        border = ft.border.all(width=2, color=ft.colors.GREY_800),
                        border_radius = 5,
                        alignment=ft.alignment.center,
                        content = ft.Column([
                            ft.Container(height=30,bgcolor='black,0.4',content=self.label,alignment=ft.alignment.center),
                            ft.Container(content=self.content_block_,expand=True,alignment=ft.alignment.center,padding=20),
                        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        )
        return self.block_draw
    def gen_inputs(self):
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