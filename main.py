import cv2
from PIL import Image as Img
from PIL import ImageTk as ImgTk
import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter.messagebox import showerror
import matplotlib.pyplot as plt
import copy

#########
def add_constant(img, constant):
    """
    Функция принимает изображение (в формате BGR) и константу в качестве параметров. Она добавляет константу к каждому пикселю
    в изображении и возвращает результат. При этом значения пикселей ограничиваются диапазоном [0, 255], чтобы удовлетворить
    ограничения для 8-битных изображений.
    """
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb_img = rgb_img.astype(np.int16) + constant
    return np.clip(rgb_img, 0, 255).astype(np.uint8)


def multiply_constant(img, constant):
    """
    Функция принимает изображение (в формате BGR) и константу в качестве параметров. Она умножает каждый пиксель в изображении на
    указанную константу и возвращает результат. При этом значения пикселей ограничиваются диапазоном [0, 255].
    """
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb_img = rgb_img.astype(np.int16) * constant
    return np.clip(rgb_img, 0, 255).astype(np.uint8)


def power_transform(img, power):
    """
    Функция принимает изображение и степень в качестве параметров. Она применяет степенное преобразование к значениям пикселей,
    возводя каждое значение в указанную степень. Результат масштабируется в диапазон [0, 255].
    """
    result = 255 * np.power(img / img.max(), power)
    return result.astype(np.uint8)


def logarithmic_transform(img):
    """
    Функция выполняет логарифмическое преобразование значений пикселей входного изображения. Обычно используется для улучшения
    контраста в темных или плохо освещенных изображениях. Преобразованное изображение масштабируется в диапазон [0, 255].
    """
    result = 255 * np.log1p(img) / np.log1p(img.max())
    return result.astype(np.uint8)


def negative(img):
    """
    Функция принимает изображение и генерирует его негатив, вычитая каждое значение пикселя из 255. Результатом является
    цветонегативное изображение.
    """
    img = np.array(255 - img)
    return img


def linear_contrast(img):
    """
    Функция выполняет линейное растяжение контраста на входном изображении. Она масштабирует значения пикселей, чтобы они
    охватывали весь диапазон [0, 255], что способствует улучшению контраста.
    """
    mn, mx = img.min(), img.max()
    result = (img - mn) / (mx - mn) * 255
    result = np.clip(result, 0, 255)
    return result.astype(np.uint8)

##hist

def build_hist(img):
    """
    Функция строит гистограмму яркости для входного изображения. Она подсчитывает, сколько пикселей имеют каждую интенсивность
    яркости и нормирует распределение на сумму всех пикселей.
    """
    h = np.zeros(256)
    for row in img:
        for g in row:
            h[g] += 1
    h /= h.sum()
    return h

def equalize(result):
    """
    Функция выполняет выравнивание гистограммы для заданного изображения. Она перераспределяет интенсивности пикселей так, чтобы
    гистограмма была равномерной, улучшая контраст изображения.
    """
    h = build_hist(result)
    sh = np.zeros(256)
    for i in range(256):
        for j in range(1, i + 1):
            sh[i] += h[j]
    for row in range(len(result)):
        for col in range(len(result[row])):
            result[row][col] = 255 * sh[result[row][col]]
    return result

def histogram_equalization(img):
    """
    Функция выполняет выравнивание гистограммы для входного изображения и возвращает результат.
    """
    result = copy.deepcopy(img)
    return equalize(result)

def histogram_equalization_rgb(img):
    """
    Функция выполняет выравнивание гистограммы для каждого канала (R, G, B) входного изображения и возвращает результатное
    изображение в формате RGB.
    """
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    r = equalize(rgb_img[:, :, 0])
    g = equalize(rgb_img[:, :, 1])
    b = equalize(rgb_img[:, :, 2])

    result = cv2.merge((r, g, b))
    return result

def histogram_equalization_hsv(img):
    """
    Функция выполняет выравнивание гистограммы для канала яркости (V) в цветовой модели HSV входного изображения и
    возвращает результатное изображение в формате RGB.
    """
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = hsv_img[:, :, 0]
    s = hsv_img[:, :, 1]
    v = equalize(hsv_img[:, :, 2])

    result = cv2.merge((h, s, v))
    return cv2.cvtColor(result, cv2.COLOR_HSV2RGB)



global filepath
filepath = ''
def get_image():
    global filepath
    filepath = ''
    filepath = filedialog.askopenfilename()
    if filepath == '':
        return
    file_path.delete(0, END)
    file_path.insert(INSERT, filepath)
    image = Img.open(filepath)
    global photo
    photo = ImgTk.PhotoImage(image.resize((500,500)))
    image = canvas.create_image(0, 0, anchor='nw',image=photo)

# Применение фильтров
def apply_filter():
    if filepath == '':
        showerror(title='Error', message='No file selected:(')
        return

    selected_filters = filter_listbox.curselection()
    if not selected_filters:
        showerror(title='Error', message='No filter selected:(')
        return

    selected_filter = filter_listbox.get(selected_filters[0])

    if selected_filter == "Original":
        image = canvas.create_image(0, 0, anchor='nw',image=photo)
    else:
        img = cv2.imread(filepath)
        if selected_filter == "Addition filter":
            user_constant = simpledialog.askfloat('Input', 'Input constant value', parent=root, initialvalue=100)
            new_img = add_constant(img, user_constant)
            new_image = Img.fromarray(new_img)
            global final1
            final1 = ImgTk.PhotoImage(new_image.resize((500,500)))
            image = canvas.create_image(0, 0, anchor='nw',image=final1)
        elif selected_filter == "Multiply filter":
            user_constant = simpledialog.askfloat('Input', 'Input constant value', parent=root, initialvalue=0.5)
            new_img = multiply_constant(img, user_constant)
            new_image = Img.fromarray(new_img)
            global final2
            final2 = ImgTk.PhotoImage(new_image.resize((500,500)))
            image = canvas.create_image(0, 0, anchor='nw',image=final2)
        elif selected_filter == "Power filter":
            user_constant = simpledialog.askfloat('Input', 'Input power value', parent=root, initialvalue=3)
            new_img = power_transform(img, user_constant)
            new_image = Img.fromarray(new_img)
            global final3
            final3 = ImgTk.PhotoImage(new_image.resize((500,500)))
            image = canvas.create_image(0, 0, anchor='nw',image=final3)
        elif selected_filter == "Log filter":
            new_img = logarithmic_transform(img)
            new_image = Img.fromarray(new_img)
            global final4
            final4 = ImgTk.PhotoImage(new_image.resize((500,500)))
            image = canvas.create_image(0, 0, anchor='nw',image=final4)
        elif selected_filter == "Negative":
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_img = negative(gray_img)
            new_image = Img.fromarray(new_img)
            global final5
            final5 = ImgTk.PhotoImage(new_image.resize((500,500)))
            image = canvas.create_image(0, 0, anchor='nw',image=final5)
        elif selected_filter == "Gist Equalizer":
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_img = histogram_equalization(gray_img)
            new_image = Img.fromarray(new_img)
            global final8
            final8 = ImgTk.PhotoImage(new_image.resize((500,500)))
            image = canvas.create_image(0, 0, anchor='nw',image=final8)
        elif selected_filter == "Lin Contrast":
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_img = linear_contrast(gray_img)
            new_image = Img.fromarray(new_img)
            global final9
            final9 = ImgTk.PhotoImage(new_image.resize((500,500)))
            image = canvas.create_image(0, 0, anchor='nw',image=final9)
        elif selected_filter == "RGB Equalizer":
            new_img = histogram_equalization_rgb(img)
            new_image = Img.fromarray(new_img)
            global final10
            final10 = ImgTk.PhotoImage(new_image.resize((500,500)))
            image = canvas.create_image(0, 0, anchor='nw',image=final10)
        elif selected_filter == "HSV Equalizer":
            new_img = histogram_equalization_hsv(img)
            new_image = Img.fromarray(new_img)
            global final11
            final11 = ImgTk.PhotoImage(new_image.resize((500,500)))
            image = canvas.create_image(0, 0, anchor='nw',image=final11)

root = Tk()
root.title("Digital image processing")
root.geometry('800x600')
root.configure(bg='#8ecae6')

# Кнопка выбора папки
btn_file_path = Button(root, text="Browse", command=get_image, width=10, bg='#023047', font=('Arial', 12, 'bold'), foreground='#FFFFFF')  # Цвета 
btn_file_path.grid(row=0, column=0, padx=20, pady=20, sticky=(W, E))

# Поле ввода папки
file_path = Entry(root, width=70, bg='#023047', font=('Arial', 12, 'bold'), foreground='#FFFFFF')  # Белый текст и цвет фона как у кнопки
file_path.grid(row=0, column=1, padx=20, pady=20, sticky=(W, E))
file_path.insert(INSERT, "Select an image...")

# Меню слева
menu_frame = Frame(root, bg='#8ecae6')
menu_frame.grid(row=1, column=0, padx=15, pady=30, sticky=(N, S))

# Список фильтров
filter_listbox = Listbox(menu_frame, selectmode=SINGLE, font=('Arial', 10, 'bold'), foreground='#FFFFFF', bg='#00BFFF', selectbackground='#FF69B4', selectforeground='#FFFFFF')  # Голубой список
filter_listbox.pack(padx=20)

filters = ["Original", "Addition filter", "Multiply filter", "Power filter", "Log filter", "Negative", "Lin Contrast", "Gist Equalizer", "RGB Equalizer", "HSV Equalizer"]
for filter_name in filters:
    filter_listbox.insert(END, filter_name)

# Кнопка для применения фильтра
apply_button = Button(menu_frame, text="Apply Filter", command=apply_filter, width=15, bg='#023047', font=('Arial', 12, 'bold'), foreground='#FFFFFF')  # Голубая кнопка
apply_button.pack(pady=20)

style = ttk.Style()
style.theme_use("default")

root.grid_rowconfigure(1, weight=1)

root.grid_columnconfigure(1, weight=1)

canvas = Canvas(root, height=500, width=500)
canvas.grid(row = 1, column = 1)

root.resizable(False, False)
root.mainloop()