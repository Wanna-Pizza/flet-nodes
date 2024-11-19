import flet as ft
import flet.canvas as cv

class CurveNode(ft.Container):
    def __init__(self, start=[0, 0], end=[0, 0]):
        super().__init__()
        self.start_x, self.start_y = start[0], start[1]
        self.end_x, self.end_y = end[0], end[1]

        self.node_in = None
        self.node_out = None

        self.content = self._content()

    def update_curve_top(self, start=[0, 0]):
        self.start_x, self.start_y = start[1], start[0]
        self.content = self._content()
        self.update()

    def update_curve_end(self, end=[0, 0]):
        self.end_x, self.end_y = end[1], end[0]
        self.content = self._content()
        self.update()

    def _content(self):
        distance = ((self.end_x - self.start_x)**2 + (self.end_y - self.start_y)**2)**0.5

        base_offset = 150

        control_offset = max(base_offset * (distance / 300), 30)

        control_x1, control_y1 = self.start_x + control_offset, self.start_y
        control_x2, control_y2 = self.end_x - control_offset, self.end_y

        self.path_elements = []
        segments = 30
        color_gradient = self._generate_color_gradient(segments)

        for i in range(segments):
            t = i / (segments - 1)
            x = (1 - t)**3 * self.start_x + 3 * (1 - t)**2 * t * control_x1 + 3 * (1 - t) * t**2 * control_x2 + t**3 * self.end_x
            y = (1 - t)**3 * self.start_y + 3 * (1 - t)**2 * t * control_y1 + 3 * (1 - t) * t**2 * control_y2 + t**3 * self.end_y

            if i > 0:
                self.path_elements.append(
                    cv.Line(
                        prev_x,
                        prev_y,
                        x,
                        y,
                        paint=ft.Paint(stroke_width=2, color=color_gradient[i - 1])
                    )
                )

            prev_x, prev_y = x, y

        self.cp = cv.Canvas(self.path_elements)
        return self.cp

    def _generate_color_gradient(self, segments):
        gradient = []

        for i in range(segments):
            ratio = i / (segments - 1)
            g = int(255 * (1 - ratio))
            r = int(255 * ratio)
            gradient.append(f"#{r:02x}{g:02x}00")

        return gradient

