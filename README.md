# Программа для рисования на Python с использованием Tkinter и Pillow
Этот проект представляет собой простую программу для рисования, разработанную на Python с 
использованием библиотек Tkinter для создания графического интерфейса и Pillow для работы с 
изображениями.

## Особенности
* __Рисование на холсте:__ Пользователи могут рисовать на белом холсте с помощью мыши.
* __Выбор цвета:__ Возможность выбора цвета кисти с помощью стандартного диалогового окна.
* __Выбор размера кисти:__ Пользователи могут выбирать размер кисти из выпадающего списка.
* __Инструмент "Ластик":__ Возможность использовать ластик для удаления нарисованных элементов.
* __Инструмент "Пипетка"__: Возможность выбирать цвет с холста, нажимая правую кнопку мыши.
* __Очистка холста:__ Кнопка для очистки всего холста.
* __Сохранение изображения:__ Возможность сохранения нарисованного изображения в формате PNG.

## Установка и запуск
### Требования
* Python 3.x
* Библиотеки:
    * tkinter (обычно поставляется с Python)
    * Pillow (для работы с изображениями)

### Установка
1. Установите библиотеку Pillow, если она еще не установлена:
``` python
pip install Pillow
```
2. Склонируйте репозиторий или скопируйте файл drawing_app.py в вашу рабочую директорию.

### Запуск
1. Перейдите в директорию с файлом __drawing_app.py__.
2. Запустите программу:
```python
python drawing_app.py
```
## Использование
1. __Рисование:__ Нажмите левую кнопку мыши и перемещайте курсор по холсту для рисования.
2. __Выбор цвета:__ Нажмите кнопку "Выбрать цвет", чтобы открыть диалоговое окно выбора цвета.
3. __Выбор размера кисти:__ Используйте выпадающий список для выбора размера кисти.
4. __Инструмент "Ластик":__ Нажмите кнопку "Ластик", чтобы переключиться на инструмент ластика. При использовании ластика 
цвет кисти становится белым, что позволяет удалять нарисованные элементы.
5. __Инструмент "Пипетка":__ Нажмите правую кнопку мыши на холсте, чтобы выбрать цвет пикселя под курсором.
6. __Очистка холста:__ Нажмите кнопку "Очистить", чтобы удалить все нарисованное.
7. __Сохранение изображения:__ Нажмите кнопку "Сохранить", чтобы сохранить текущее изображение
в формате PNG.

## Структура проекта
* __drawing_app.py:__ Основной файл программы, содержащий код для создания графического
интерфейса и функциональности рисования.

### Пример кода
```python
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw

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

        self.setup_ui()

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)  # Привязка события для пипетки

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

    def choose_color(self):
        self.previous_color = self.pen_color  # Сохраняем текущий цвет
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
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

    def pick_color(self, event):
        x = event.x
        y = event.y
        color = self.image.getpixel((x, y))  # Получаем цвет пикселя
        self.pen_color = '#%02x%02x%02x' % color  # Преобразуем цвет в формат HEX

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Автор
Вереин Михаил Павлович
verein83@mail.ru

### Благодарности
Tkinter и Pillow разработчикам за предоставленные библиотеки.

Сообществу Python за поддержку и ресурсы.
_____
__Приятного рисования!__
