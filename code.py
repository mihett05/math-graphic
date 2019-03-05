from tkinter import *
from numpy import arange
from collections import namedtuple
from math import *
from PIL import Image, ImageDraw

root = Tk()  # initialization
root.resizable(width=False, height=False)  # turn off window's resizable
root.title("Math Graphic")
root.iconbitmap('graphic.ico')

bg = namedtuple("bg", ["color"])(color="#DCDCDC")
string = namedtuple("string", ["color", "font"])(color="#696969", font="Arial 14")

width, height = 900, 900
center = (int(width/2), int(height/2))  # center of the graphic

table = [center, center]  # table with values
unit = 30  # size of on cell


def build(event):
    global table
    c.delete("line")  # clear graphic
    text = func.get("1.0", END)  # gets text from y's function
    text = text.replace("^", "**").replace(",", ".")
    tasks = text.split(";")
    y = lambda x, code: eval(code) * -1
    for task in tasks:
        if "**" not in task and "/" not in task and "cos" not in task and "sin" not in task and "tan"\
                not in task and "sqrt" not in task:
            table = [(15, y(15, task)), (-15, y(-15, task))]  # make new values's tables
            c.create_line(center[0] + table[0][0] * unit, center[1] + table[0][1] * unit,
                          center[0] + table[1][0] * unit, center[1] + table[1][1] * unit,
                          width=2, tag="line")  # make new line
        else:  # for square function
            table = [(x, y(x, task)) for x in arange(-15, 15, 0.001)]
            for j in range(len(table))[:-2]:
                c.create_line(center[0] + table[j][0] * unit, center[1] + table[j][1] * unit,
                              center[0] + table[j + 1][0] * unit, center[1] + table[j + 1][1] * unit,
                              width=2, tag="line")
            c.create_line(center[0] + table[-2][0] * unit, center[1] + table[-1][1] * unit,
                          center[0] + table[-1][0] * unit, center[1] + table[-2][1] * unit,
                          width=2, tag="line")


def export(event):
    global table
    text = func.get("1.0", END)
    text = text.replace("^", "**").replace(",", ".")
    tasks = text.split(";")
    y = lambda x, code: eval(code) * -1
    im = Image.new("RGB", (width, height), (255, 255, 255))  # (220, 220, 220))
    dr = ImageDraw.Draw(im)
    for i in range(int(width / unit)):  # draws background cell
        dr.line([i * unit, 0, i * unit, height], fill=(220, 220, 220))
        dr.line([0, i * unit, width, i * unit], fill=(220, 220, 220))
        if i == 15:
            dr.text((i * unit - 10, height / 2 + 10), text=str(counter[i]), fill=string.color)
        else:
            dr.text((i * unit, height / 2 + 10), text=str(counter[i]), fill=(105, 105, 105))  # y
            dr.text((width / 2 - 20, i * unit), text=str(r_counter[i]), fill=(105, 105, 105))  # x
    graphic_bg = [(center, (width, height / 2)), (center, (width / 2, 0)), (center, (0, height / 2)),
                  (center, (width / 2, height))]  # values for graphic background
    for point in graphic_bg:
        dr.line(point, width=2, fill=(0, 0, 0))  # draws graphic background
    for task in tasks:
        if "**" not in task and "/" not in task and "cos" not in task and "sin" not in task and "tan"\
                not in task and "sqrt" not in task:
            table = [(15, y(15, task)), (-15, y(-15, task))]  # make new values's tables
            dr.line([center[0] + table[0][0] * unit, center[1] + table[0][1] * unit,
                     center[0] + table[1][0] * unit, center[1] + table[1][1] * unit],
                    fill=(0, 0, 0), width=2)  # make new line
        else:  # for square function
            table = [(x, y(x, task)) for x in arange(-15, 15, 0.001)]
            for j in range(len(table))[:-2]:
                dr.line([center[0] + table[j][0] * unit, center[1] + table[j][1] * unit,
                         center[0] + table[j + 1][0] * unit, center[1] + table[j + 1][1] * unit],
                        width=2, fill=(0, 0, 0))
            dr.line([center[0] + table[-2][0] * unit, center[1] + table[-1][1] * unit,
                     center[0] + table[-1][0] * unit, center[1] + table[-2][1] * unit],
                    width=2, fill=(0, 0, 0))
    im.save("line.png", "PNG")


frame = Frame(root)  # make frame
frame.pack(fill=X)

label = Label(frame, text="y = ", width=4, font=string.font)
label.pack(side=LEFT)  # make label

func = Text(frame, height=1, width=40, font=string.font, wrap=WORD)
func.pack(side=LEFT, anchor=N)  # make textfield for x function

build_btn = Button(frame, text="Build", width=7, font=string.font)
build_btn.pack(side=RIGHT)
build_btn.bind("<Button-1>", build)  # make build button

build_btn = Button(frame, text="Export", width=7, font=string.font)
build_btn.pack(side=RIGHT)
build_btn.bind("<Button-1>", export)  # make export button

clear_btn = Button(frame, text="Clear", width=7, font=string.font, command=lambda: c.delete("line"))
clear_btn.pack(side=RIGHT)  # make clear button


c = Canvas(root, width=width, height=height, bg='white')
c.pack()

counter = [i for i in range(-15, int(width / unit) + 1 - 15)]
r_counter = counter[::-1]
counter[0], r_counter[0] = "", ""

for i in range(int(width / unit)):  # draws background cell
    c.create_line((i * unit, 0), (i * unit, height), fill=bg.color)
    c.create_line((0, i * unit), (width, i * unit), fill=bg.color)
    if i == 15:
        c.create_text((i * unit - 10, height / 2 + 10), text=str(counter[i]), fill=string.color)
    else:
        c.create_text((i * unit, height / 2 + 10), text=str(counter[i]), fill=string.color)  # y
        c.create_text((width / 2 - 12, i * unit), text=str(r_counter[i]), fill=string.color)  # x

graphic_bg = [(center, (width, height/2)), (center, (width / 2, 0)), (center, (0, height/2)),
              (center, (width/2, height))]  # values for graphic background
for point in graphic_bg:
    c.create_line(point, width=2)  # draws graphic background

c.create_line(center[0] + table[0][0] * 30, center[1] + table[0][1] * 30,
              center[0] + table[1][0] * 30, center[1] + table[1][1] * 30,
              width=2, tag="line")  # make new line
root.mainloop()
