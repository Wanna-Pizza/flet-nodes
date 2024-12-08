import flet as ft

from Node import Node
from Nodes.TextNode import TextNode


class view_node(ft.Stack):
    def __init__(self):
        super().__init__()
        self.hover_x = 0
        self.hover_y = 0
        self.connections = []
        self.nodes()
        self.controls = [self._content()]
    
    async def update_node(self,node, scale_factor):
        if isinstance(node,Node):
            node.update_block_drawer(scale_factor)
    


    def vert_update(self, e: ft.DragUpdateEvent):
        self.ges.top = self.ges.top + e.delta_y*self.ges.scale
        self.ges.left = self.ges.left + e.delta_x*self.ges.scale
        self.update()
    
    def scale_square(self,left_top_x, left_top_y, size, scale):
        center_x = left_top_x + size / 2
        center_y = left_top_y + size / 2
        
        new_size = size * scale
        
        new_left_top_x = center_x - new_size / 2
        new_left_top_y = center_y - new_size / 2
        
        return new_left_top_x, new_left_top_y

    def reverse_scale_square(self,new_left_top_x, new_left_top_y, new_size, scale):
        center_x = new_left_top_x + new_size / 2
        center_y = new_left_top_y + new_size / 2
        
        old_size = new_size / scale
        
        old_left_top_x = center_x - old_size / 2
        old_left_top_y = center_y - old_size / 2
        
        return old_left_top_x, old_left_top_y, old_size

    def get_size(self):
        original_w = self.ges.width
        new_w = self.ges.width*self.ges.scale
        diff_w = original_w-new_w
        w_scaled = original_w-diff_w

        original_h = self.ges.height
        new_h = self.ges.height*self.ges.scale
        diff_h = original_h-new_h
        h_scaled = original_h-diff_h

        return w_scaled,h_scaled

            
    def zoom_async(self, e: ft.ScrollEvent):
        scale_step = 0.05
        
        scale_def = self.ges.scale
        if e.scroll_delta_y < 0:
            self.ges.scale += scale_step

        elif e.scroll_delta_y > 0:
            self.ges.scale -= scale_step
        
        view_h = self.page.window.height
        view_w = self.page.window.width

        center_x = view_w / 2
        center_y = view_h / 2
        
        # # w,h = self.get_size()
        # # x,y = self.scale_square(left_top_x=self.ges.left,left_top_y=self.ges.top,size=self.ges.width,scale=self.ges.scale)
        

        # delta_x = x - center_x
        # delta_y = y - center_y

        # x,y,scale = self.reverse_scale_square(new_left_top_x=delta_x,new_left_top_y=delta_y,new_size=w,scale=w/self.ges.width)

        self.update()
        self.ges.update()






        
    def hover(self,e:ft.HoverEvent):
        self.hover_x = e.local_x
        self.hover_y = e.local_y

        self.hover_g_x = e.global_x
        self.hover_g_y = e.global_y
        
    
    def zoom(self,e):
        self.zoom_async(e)


    def _content(self):
        self.view = ft.Container(border=ft.border.all(width=3,color='white,0.3'),padding=0)
        self.stack_control = ft.Stack([self.node1,self.node2])
        self.view.content = self.stack_control
        self.ges = ft.GestureDetector(
            content=self.view,
            on_vertical_drag_update=self.vert_update,
            top=0,left=0,
            on_scroll=self.zoom,
            on_hover=self.hover,
            width=1920,
            height=1080,
            scale=1
            
            )
        
        return self.ges

    def nodes(self):
        self.node1 = TextNode(top=100, left=500)
        self.node2 = TextNode(top=350, left=10)
        


def main(page: ft.Page):
    page.padding = 0
    page.update()
    page.add(view_node())
    


ft.app(main)