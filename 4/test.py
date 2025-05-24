"""
Необходимо визуально изобразить предложенную задачу. 
1. Диски
на шпинделях сделать случайных цветов. На каждом диске
отображать цифру, равную его диаметру. Диаметр диска также
показывать его фактическим размером в пикселях.
 
Существует 8 шпинделей, пронумерованых от 8 до 1 слева направо. На
каждом шпинделе надеты диски, в количестве, равном соответствующей
цифре из ID студента. Все диски имеют разные диаметры. Диаметр диска
равен M * 10 + N, где М – номер шпинделя, на котором надет диск, а N –
это номер диска на шпинделе, считая сверху вниз.
 
Задача
а) За одну итерацию можно переместить не более одного диска
б) Диски можно класть только с большего на меньший
в) Со шпинделя номер 8 можно перекладывать диски только на шпиндели 7 и 6
г) Со шпинделя номер 1 можно перекладывать диски только на шпиндели номер 2 и 3
д) Со шпинделей от 2 по 7 можно перекладывать диски только на два соседних шпинделя.
 
"""
import random
import sys
from random import random as rnd
from random import randint
from tkinter import Tk, Canvas, Frame, BOTH, Text, Button, Label, BOTTOM
import copy
 
rings = 30
h = 10
x0 = 100
y0 = rings * h + 50
step = 130
const_w = 10
hide = "#f8f4ff"
show = "#ff0000"
 
 
class Demo(Frame):
    def __init__(self):
        super(Demo, self).__init__()
        self.id_student = "70194603"
        self.log_matrix = list()
        self.state = list()
        self.step = 0
        self.canvas = Canvas(self.master)
        self.input_id = Text(self.master, height=12, width=40)
 
        self.b_get_id = Button(self.master, text="Отобразить", command=self.get_id)
        self.b_start = Button(self.master, text="Начать", command=self.draw_p0)
        self.b_p1 = Button(self.master, text="П.1", command=self.draw_p1)
        self.b_p2 = Button(self.master, text="П.2", command=self.draw_p2)
        self.b_p3 = Button(self.master, text="П.3", command=self.draw_p3)
        self.b_p4 = Button(self.master, text="П.4", command=self.draw_p4)
        self.b_end = Button(self.master, text="Окончить", command=self.draw_end)
 
        x = step * 8 + 120
        y = 50
        H = 50
 
        self.b_get_id.place(x=x, y=y, width=120, height=40)
        self.b_start.place(x=x, y=y+H, width=120, height=40)
        self.b_p1.place(x=x, y=y+2*H, width=50, height=40)
        self.b_p2.place(x=x, y=y+3*H, width=50, height=40)
        self.b_p3.place(x=x, y=y+4*H, width=50, height=40)
        self.b_p4.place(x=x, y=y+5*H, width=50, height=40)
        self.b_end.place(x=x, y=y+6*H, width=120, height=40)
        self.input_id.place(x=x, y=y+7*H, width=120, height=40)
 
        self.t_p1 = Text(self.master)
        self.t_p2 = Text(self.master)
        self.t_p3 = Text(self.master)
        self.t_p4 = Text(self.master)
 
        self.t_p1.place(x=x+70, y=y+2*H, width=50, height=40)
        self.t_p2.place(x=x+70, y=y+3*H, width=50, height=40)
        self.t_p3.place(x=x+70, y=y+4*H, width=50, height=40)
        self.t_p4.place(x=x+70, y=y+5*H, width=50, height=40)
 
        self.list_labels = list()
        max_item = 9
        for row in range(8*max_item):
            line = list()
            for tower in range(8):
                label = Label(self.master, text="0")
                x = x0 - step/2 + tower * step
                y = y0 - (row + 1) * h
                label.config(font=("Courier", 7))
                label.place(x=x, y=y, width=10, height=7)
                label["fg"] = self["bg"]
                line.append(label)
            self.list_labels.append(line)
 
        self.matrix = [[(0, "ff0000") for _ in range(8)] for _ in range(72)]
        self.create_matrix()
        self.draw_matrix()
        self.flag = False
 
    def get_id(self):
        text = self.input_id.get("1.0", "end").replace("\n", "")
        if len(text) == 8 and text.isdigit():
            self.id_student = text
        self.create_matrix()
        self.draw_matrix()
 
    def create_matrix(self):
        self.matrix = [[(0, "#000000") for _ in range(8)] for _ in range(72)]
        for tower in range(8):
            for row in range(int(self.id_student[tower])):
                n = int(self.id_student[tower]) - row
                color = f"#{random.randint(100000, 999999)}"
                self.matrix[row][tower] = ((tower+1) * const_w + n, color)
 
    def draw_matrix(self):
        self.canvas.delete("all")
        self.draw_towers()
        for tower in range(8):
            for row in range(rings):
                if self.matrix[row][tower][0] == 0:
                    self.list_labels[row][tower].config(text="0")
                    self.list_labels[row][tower].config(fg=self["bg"])
                    self.list_labels[row][tower].config(state='normal')
                    self.canvas.pack(fill=BOTH, expand=1)
                    continue
                line = self.matrix[row][tower]
                w = line[0]
                color = line[1]
                x = x0 + tower * step - w / 2
                y = y0 - h * (row + 1)
                self.canvas.create_rectangle(x, y, x+w, y+h, outline=color, fill=color)
                self.canvas.pack(fill=BOTH, expand=1)
                self.list_labels[row][tower].config(text=str(w))
                self.list_labels[row][tower].config(fg=show)
                self.list_labels[row][tower].config(state='normal')
        self.canvas.pack(fill=BOTH, expand=1)
 
    def draw_towers(self):
        color = "#ffffff"
        w = 200
        H = rings * h
        x1 = x0+step*8
        y1 = y0+10
 
        self.canvas.create_rectangle(x0-50, y0, x1, y1, outline="#fb0", fill=color)
        self.canvas.pack(fill=BOTH, expand=1)
        for i in range(8):
            x1 = int(x0 - 3 + i * step)
            y1 = int(y0 - H)
            x2 = x1 + 6
            y2 = y0
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="#fb0", fill=color)
            self.canvas.pack(fill=BOTH, expand=1)
 
    def draw_p0(self):
        per = 0
        self.draw_p(0)
 
    def draw_p1(self):
        per = int(self.t_p1.get("1.0", "end"))
        self.draw_p(per)
 
    def draw_p2(self):
        per = int(self.t_p2.get("1.0", "end"))
        self.draw_p(per)
 
    def draw_p3(self):
        per = int(self.t_p3.get("1.0", "end"))
        self.draw_p(per)
 
    def draw_p4(self):
        per = int(self.t_p4.get("1.0", "end"))
        self.draw_p(per)
 
    def draw_end(self):
        per = 100
        self.draw_p(per)
 
    def draw_p(self, p):
        self.create_matrix()
        count_steps = {
            "1": 1, "2": 4, "3": 8, "4": 16, "5": 32, "6": 64, "7": 127, "8": 255, "9": 511
        }
        p = p / 100
        n = int(self.id_student[-1])
        self.step = int(count_steps[str(n)] * p)
        self.calculate()
 
    def calculate(self):
        self.get_id()
        n = int(self.id_student[-1])
        self.id_student = "0000000" + str(n)
        self.create_matrix()
        self.move_tower(n, 8, 6, 7)
 
    def move_tower(self, n, point1, point2, temp):
        if n == 0:
            return
        self.move_tower(n - 1, point1, temp, point2)
        self.move(point1, point2)
        self.move_tower(n - 1, temp, point2, point1)
        return
 
    def move(self, from_, to):
        empty = (0, "#000000")
        i_s = 0
        while self.matrix[i_s+1][from_ - 1][0] > 0:
            i_s += 1
        item = self.matrix[i_s][from_ - 1]
        i_t = 0
        while self.matrix[i_t][to - 1][0] > 0:
            i_t += 1
 
        self.matrix[i_t][to-1] = item
        self.matrix[i_s][from_-1] = empty
        self.step -= 1
        if self.step <= 0:
            self.draw_matrix()
            self.step = 10000
 
 
if __name__ == '__main__':
    root = Tk()
    ex = Demo()
    w = step * 10 + 30
    H = h * rings + 20 + 200
    root.geometry(f"{w}x{H}")
    root.mainloop()