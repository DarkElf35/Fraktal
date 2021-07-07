import tkinter as tk
from math import cos
from math import sin
from math import sqrt
from math import pi


lineId = None
KRUG_ID = None
draw_line = True
x_start_crug = 0
y_start_crug = 0


def mouseMove(event):
    label.configure(text=f"x={event.x}, y={event.y}")
    global Circle_curr
    global Circle_prev
    if draw_line:
        if lineId:
            x1, y1, *_ = canvas.coords(lineId)
            canvas.coords(lineId, x1, y1, event.x, event.y)

    if draw_line == False:
        if KRUG_ID:
            canvas.coords(KRUG_ID, x_start_crug, y_start_crug, event.x, event.y)


def mouseClick(event):
    global lineId
    global KRUG_ID

    if draw_line:
        if lineId:
            lineId = None
        else:
            lineId = canvas.create_line(event.x, event.y, event.x, event.y,
                                        fill=lineColor.get())
    if draw_line == False:
        if KRUG_ID:
            KRUG_ID = None
        else:
            global x_start_crug
            global y_start_crug
            x_start_crug = event.x
            y_start_crug = event.y
            KRUG_ID = canvas.create_oval(event.x, event.y, event.x, event.y,
                                         fill=lineColor.get())


def drawImage(x1, y1, x2, y2):
    if x2 - x1 <= 1:
        return
    d = (x2 - x1) / 3
    canvas.create_rectangle(x1 + d, y1 + d, x1 + 2 * d, y1 + 2 * d)
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1: continue
            drawImage(x1 + d * i, y1 + d * j, x1 + d * i + d, y1 + d * j + d)


def drawKantor(x, y, n, rozmir):
    if n - 1 > 0:
        z = rozmir / 2
        drawKantor(x - rozmir, y + rozmir, n - 1, z)
        drawKantor(x - rozmir, y - rozmir, n - 1, z)
        drawKantor(x + rozmir, y + rozmir, n - 1, z)
        drawKantor(x + rozmir, y - rozmir, n - 1, z)

    canvas.create_rectangle(x - rozmir, y - rozmir, x + rozmir, y + rozmir)


def draw_Pifagor_rect(x1, y1, l, a1):
    prevX_1 = x1
    prevY_1 = y1
    canvas.create_line(prevX_1, prevY_1, x1 + round(l * cos(a1)), y1 - round(l * sin(a1)))

    prevX_2 = x1 + round(l * cos(a1))
    prevY_2 = y1 - round(l * sin(a1))
    canvas.create_line(prevX_2, prevY_2, x1 + round(l * sqrt(2) * cos(a1 + pi / 4)),
                       y1 - round(l * sqrt(2) * sin(a1 + pi / 4)))

    prevX_3 = x1 + round(l * sqrt(2) * cos(a1 + pi / 4))
    prevY_3 = y1 - round(l * sqrt(2) * sin(a1 + pi / 4))
    canvas.create_line(prevX_3, prevY_3, x1 + round(l * cos(a1 + pi / 2)), y1 - round(l * sin(a1 + pi / 2)))

    prevX_4 = x1 + round(l * cos(a1 + pi / 2))
    prevY_4 = y1 - round(l * sin(a1 + pi / 2))
    canvas.create_line(prevX_4, prevY_4, x1, y1)


def draw_Pifagor_tree(x, y, l, a):
    if l > 4:
        draw_Pifagor_rect(round(x), round(y), round(l), a)
        draw_Pifagor_tree(x - l * sin(a), y - l * cos(a), l / sqrt(2), a + pi / 4)
        draw_Pifagor_tree(x - l * sin(a) + l / sqrt(2) * cos(a + pi / 4),
                          y - l * cos(a) - l / sqrt(2) * sin(a + pi / 4), l / sqrt(2), a - pi / 4)


def buttonClick():
    drawImage(0, 0, canvas.winfo_width(), canvas.winfo_height())


def buttonClick1():
    drawKantor(250, 250, 3, 130)


def buttonClick2():
    draw_Pifagor_tree(210, 400, 85, 0)


def buttonClick3():
    global draw_line
    if draw_line:
        btn3.config(text='Окружность')
        draw_line = False
    else:
        btn3.config(text='Линия')
        draw_line = True


def clear():
    canvas.delete("all")


window = tk.Tk()
window.title('Hello!')
window.geometry('650x800')

lineColor = tk.StringVar()
lineColor.set("green")

btn = tk.Button(window, text="Ковер Серпинского", command=buttonClick)
btn1 = tk.Button(window, text="Множество Кантора", command=buttonClick1)
btn2 = tk.Button(window, text="Дерево Пифагора", command=buttonClick2)
btn3 = tk.Button(window, text="Линия", command=buttonClick3)
btn.pack(pady=5)
btn1.pack(pady=5)
btn2.pack(pady=5)
btn3.pack(pady=5)

canvas = tk.Canvas(window, bg="white", width=500, height=500)
canvas.pack()
canvas.bind('<Motion>', mouseMove)
canvas.bind('<Button-1>', mouseClick)

label = tk.Label(window)
label.config(font=("Courier", 24))
label.pack()

rad1 = tk.Radiobutton(window, text="Зеленый", bg="green",
                      value="green", var=lineColor)
rad1.pack()
rad2 = tk.Radiobutton(window, text="Красный", bg="red",
                      value="red", var=lineColor)
rad2.pack()

menu = tk.Menu(window)
new_item = tk.Menu(menu)
new_item.add_command(label='Очистить', command=clear)
menu.add_cascade(label='Файл', menu=new_item)
window.config(menu=menu)

window.mainloop()