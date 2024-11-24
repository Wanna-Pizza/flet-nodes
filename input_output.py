import flet as ft

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
        self.stack = self.node.stack
        print(F'ID INPUT: {self.id_}')
        self.update_offsets()
        
        return super().did_mount()