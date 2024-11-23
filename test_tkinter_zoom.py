import tkinter as tk

class ZoomApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()

        # Рисуем начальный прямоугольник
        self.rect = self.canvas.create_rectangle(150, 100, 450, 300, fill="blue")

        self.scale = 1.0  # Начальный масштаб
        self.canvas.bind("<MouseWheel>", self.zoom)

    def zoom(self, event):
        # Изменение масштаба при прокрутке мыши
        scale_factor = 1.1 if event.delta > 0 else 0.9
        self.scale *= scale_factor

        # Получаем координаты центра мышки
        mouse_x = self.canvas.canvasx(event.x)
        mouse_y = self.canvas.canvasy(event.y)

        # Масштабируем прямоугольник
        self.canvas.scale(self.rect, mouse_x, mouse_y, scale_factor, scale_factor)

        # Перерисовываем канвас с новым масштабом
        self.canvas.config(scrollregion=self.canvas.bbox(self.rect))

if __name__ == "__main__":
    root = tk.Tk()
    app = ZoomApp(root)
    root.mainloop()
