import flet as ft
import flet.canvas as cv

class CurveNode(ft.Container):
    def __init__(self, 
                 start=[0, 0], 
                 end=[0, 0], 
                 start_color="#ffffff",
                 end_color="#ff0000",
                 node_in=None,
                 node_out=None,
                 id_in=0,
                 id_out=0 
                 
                 ):
        super().__init__()
        self.id_input = id_in
        self.id_output = id_out
        self.start_x, self.start_y = start[0], start[1]
        self.end_x, self.end_y = end[0], end[1]
        self.color_gradient = None

        self.segments = 20

        self.start_color = start_color
        self.end_color = end_color

        self.node_in = node_in
        self.node_out = node_out
        self.content = self._content()

    def update_curve_top(self,x,y):
        self.start_x, self.start_y = x,y
        self._update_curve()

    def update_curve_end(self,x,y):
        self.end_x, self.end_y = x, y
        self._update_curve()

    def set_colors(self, start_color, end_color):
        self.start_color = start_color
        self.end_color = end_color
        self.content = self._content()
        self.update()

    def _content(self):
        distance = ((self.end_x - self.start_x)**2 + (self.end_y - self.start_y)**2)**0.5

        base_offset = 150

        control_offset = max(base_offset * (distance / 300), 30)

        control_x1, control_y1 = self.start_x + control_offset, self.start_y
        control_x2, control_y2 = self.end_x - control_offset, self.end_y

        self.path_elements = []
        self.color_gradient = self._generate_color_gradient(self.start_color, self.end_color, self.segments)

        for i in range(self.segments):
            t = i / (self.segments - 1)
            x = (1 - t)**3 * self.start_x + 3 * (1 - t)**2 * t * control_x1 + 3 * (1 - t) * t**2 * control_x2 + t**3 * self.end_x
            y = (1 - t)**3 * self.start_y + 3 * (1 - t)**2 * t * control_y1 + 3 * (1 - t) * t**2 * control_y2 + t**3 * self.end_y

            if i > 0:
                self.path_elements.append(
                    cv.Line(
                        prev_x,
                        prev_y,
                        x,
                        y,
                        paint=ft.Paint(stroke_width=2, color=self.color_gradient[i - 1])
                    )
                )

            prev_x, prev_y = x, y

        self.cp = cv.Canvas(self.path_elements)
        return self.cp



    def _update_curve(self):
        distance = ((self.end_x - self.start_x)**2 + (self.end_y - self.start_y)**2)**0.5
        base_offset = 150
        control_offset = max(base_offset * (distance / 300), 30)

        control_x1, control_y1 = self.start_x + control_offset, self.start_y
        control_x2, control_y2 = self.end_x - control_offset, self.end_y
        
        prev_x, prev_y = self.start_x, self.start_y
        line_idx = 0

        for i in range(self.segments):
            t = i / (self.segments - 1)
            t_squared = t * t
            t_cubed = t_squared * t
            one_minus_t = 1 - t
            one_minus_t_squared = one_minus_t * one_minus_t
            one_minus_t_cubed = one_minus_t_squared * one_minus_t

            x = (one_minus_t_cubed * self.start_x +
                3 * one_minus_t_squared * t * control_x1 +
                3 * one_minus_t * t_squared * control_x2 +
                t_cubed * self.end_x)

            y = (one_minus_t_cubed * self.start_y +
                3 * one_minus_t_squared * t * control_y1 +
                3 * one_minus_t * t_squared * control_y2 +
                t_cubed * self.end_y)

            if i > 0:
                line = self.cp.shapes[line_idx]
                line.x1, line.y1 = prev_x, prev_y
                line.x2, line.y2 = x, y
                line_idx += 1

            prev_x, prev_y = x, y

        self.cp.update()






    def _generate_color_gradient(self, start_color, end_color, segments):
        def hex_to_rgb(hex_color):
            return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

        def rgb_to_hex(rgb):
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)

        gradient = []

        for i in range(self.segments):
            ratio = i / (self.segments - 1)
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            gradient.append(rgb_to_hex((r, g, b)))

        return gradient
    def did_mount(self):
        return super().did_mount()