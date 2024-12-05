import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageFont

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.brush_size = 1  # Изначальный размер кисти
        self.previous_color = self.pen_color  # Сохраняем предыдущий цвет
        self.text_mode = False  # Флаг для режима текста

        self.setup_ui()

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)  # Привязка события для пипетки
        self.canvas.bind('<Button-1>', self.place_text)  # Привязка события для размещения текста

        # Привязка горячих клавиш
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Кнопка для переключения на ластик
        eraser_button = tk.Button(control_frame, text="Ластик", command=self.toggle_eraser)
        eraser_button.pack(side=tk.LEFT)

        # Выпадающий список для выбора размера кисти
        self.brush_size_var = tk.IntVar(value=self.brush_size)
        sizes = [1, 2, 5, 10]
        brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *sizes, command=self.update_brush_size)
        brush_size_menu.pack(side=tk.LEFT)

        # Предварительный просмотр цвета кисти
        self.color_preview = tk.Canvas(control_frame, width=30, height=30, bg=self.pen_color)
        self.color_preview.pack(side=tk.LEFT, padx=5)

        # Кнопка для изменения размера холста
        resize_button = tk.Button(control_frame, text="Изменить размер холста", command=self.resize_canvas)
        resize_button.pack(side=tk.LEFT)

        # Кнопка для добавления текста
        text_button = tk.Button(control_frame, text="Текст", command=self.enter_text_mode)
        text_button.pack(side=tk.LEFT)

        # Кнопка для изменения цвета фона
        change_bg_button = tk.Button(control_frame, text="Изменить фон", command=self.change_background_color)
        change_bg_button.pack(side=tk.LEFT)

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        self.previous_color = self.pen_color  # Сохраняем текущий цвет
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.update_color_preview()  # Обновляем предварительный просмотр цвета

    def save_image(self, event=None):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def update_brush_size(self, size):
        self.brush_size = int(size)

    def toggle_eraser(self):
        if self.pen_color == "white":
            # Возвращаем предыдущий цвет
            self.pen_color = self.previous_color
        else:
            # Сохраняем текущий цвет и переключаем на ластик
            self.previous_color = self.pen_color
            self.pen_color = "white"
        self.update_color_preview()  # Обновляем предварительный просмотр цвета

    def pick_color(self, event):
        x = event.x
        y = event.y
        color = self.image.getpixel((x, y))  # Получаем цвет пикселя
        self.pen_color = '#%02x%02x%02x' % color  # Преобразуем цвет в формат HEX
        self.update_color_preview()  # Обновляем предварительный просмотр цвета

    def update_color_preview(self):
        self.color_preview.config(bg=self.pen_color)

    def resize_canvas(self):
        width = simpledialog.askinteger("Изменить размер холста", "Введите ширину:", minvalue=1, maxvalue=2000)
        height = simpledialog.askinteger("Изменить размер холста", "Введите высоту:", minvalue=1, maxvalue=2000)
        if width and height:
            self.canvas.config(width=width, height=height)
            self.image = Image.new("RGB", (width, height), "white")
            self.draw = ImageDraw.Draw(self.image)

    def enter_text_mode(self):
        self.text_mode = True
        self.text = simpledialog.askstring("Введите текст", "Введите текст:")
        if self.text:
            self.canvas.bind('<Button-1>', self.place_text)

    def place_text(self, event):
        if self.text_mode and self.text:
            x, y = event.x, event.y
            self.canvas.create_text(x, y, text=self.text, fill=self.pen_color, font=("Arial", 12))
            self.draw.text((x, y), self.text, fill=self.pen_color, font=ImageFont.truetype("arial.ttf", 12))
            self.text_mode = False
            self.canvas.unbind('<Button-1>')

    def change_background_color(self):
        new_color = colorchooser.askcolor()[1]
        if new_color:
            self.canvas.config(background=new_color)
            self.image = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), new_color)
            self.draw = ImageDraw.Draw(self.image)

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()