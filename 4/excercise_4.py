import tkinter as tk
from tkinter import Frame, Canvas, Text, Button, BOTH, Label
import random
from copy import deepcopy

RINGS = 30
STEP = 130
DISK_HEIGHT = 10
x0 = 100
y0 = RINGS * DISK_HEIGHT + 50
SHOW_LABEL= "#ff0000"

allowed_transitions = {
  1: [2, 3],
  2: [1, 3],
  3: [2, 4],
  4: [3, 5],
  5: [4, 6],
  6: [5, 7],
  7: [6, 8],
  8: [6, 7]
}

class App(Frame):
  def __init__(self):
    super(App, self).__init__()
    self.master.title('Ханойские башни')
    self.student_id = '70194603'
    self.disks = [] # [(31, '#348755'), 0, 2] disk_data, row, tower
    self.total_iterations = 0
    self.current_iteration = 0
    self.iterations_log = []
    self.initial_disks = []
    self.floating_disk = () # [(31, '#348755'), 0, 2] disk_data, from_, old_row, to_

    self.canvas = Canvas(self.master)
    self.input_id = Text(self.master, height=12, width=40)
    self.input_id.insert("1.0", self.student_id)

    self.button_start = Button(self.master, text="Начало", command=self.get_initial_state)
    self.button_pos1 = Button(self.master, text="П.1", command=self.draw_pos1)
    self.button_pos2 = Button(self.master, text="П.2", command=self.draw_pos2)
    self.button_pos3 = Button(self.master, text="П.3", command=self.draw_pos3)
    self.button_pos4 = Button(self.master, text="П.4", command=self.draw_pos4)
    self.button_end = Button(self.master, text="Окончить", command=self.draw_end)

    self.current_iteration_label = Label(self.master, text=f"Текущая итерация {self.current_iteration}")
    self.current_iteration_label.place(x=x0, y=y0 + 40, width=200, height=20)

    cnt = 8
    for i in range(8):
      label = Label(self.master, text=str(cnt-i))
      label.place(x=x0 + i * STEP - 10, y=y0 + 15, width=20, height=20)

    x = (STEP * 8 + 120)/2
    y = DISK_HEIGHT + 440
    H = 50

    self.button_start.place(x=x-H, y=y-20, width=120, height=40)
    self.button_pos1.place(x=x+2*H, y=y, width=50, height=40)
    self.button_pos2.place(x=x+3*H, y=y, width=50, height=40)
    self.button_pos3.place(x=x+4*H, y=y, width=50, height=40)
    self.button_pos4.place(x=x+5*H, y=y, width=50, height=40)
    self.button_end.place(x=x+6*H, y=y-20, width=120, height=40)
    self.input_id.place(x=x+9*H, y=y-20, width=120, height=40)

    self.input_pos1 = Text(self.master)
    self.input_pos2 = Text(self.master)
    self.input_pos3 = Text(self.master)
    self.input_pos4 = Text(self.master)

    self.input_pos1.insert("1.0", int(self.student_id[0:2]))
    self.input_pos2.insert("1.0", int(self.student_id[2:4]))
    self.input_pos3.insert("1.0", int(self.student_id[4:6]))
    self.input_pos4.insert("1.0", int(self.student_id[6:8]))

    self.input_pos1.place(x=x+2*H, y=y-40, width=50, height=40)
    self.input_pos2.place(x=x+3*H, y=y-40, width=50, height=40)
    self.input_pos3.place(x=x+4*H, y=y-40, width=50, height=40)
    self.input_pos4.place(x=x+5*H, y=y-40, width=50, height=40)

    self.get_initial_state()
    self.total_iterations = self.calculate_total_iterations()
    print(f"Общее количество итераций: {self.total_iterations}")
    self.flag = False
 
  def get_initial_state(self):
    text = self.input_id.get("1.0", "end").replace("\n", "")
    if len(text) == 8 and text.isdigit():
        self.student_id = text
    self.init_towers()
    self.draw_towers()

  def init_towers(self, make_colors=True):
    self.towers = [[(0, "#000000") for _ in range(8)] for _ in range(72)]
    for tower in range(8):
      for row in range(int(self.student_id[tower])):
        m = tower + 1
        n = int(self.student_id[tower]) - row
        if make_colors:
          color = f"#{random.randint(100000, 999999)}"
        self.towers[row][tower] = (m * 10 + n, color)
        self.disks.append([self.towers[row][tower], row, tower])

    self.floating_disk = ()
    self.initial_towers = deepcopy(self.towers)
    self.disks = sorted(self.disks, key=lambda x: x[0])

  def draw_towers(self):
    self.canvas.delete("all")
    self.draw_base()
    for display_tower in range(8):
      real_tower = 7 - display_tower
      for row in range(RINGS):
        if self.towers[row][real_tower][0] == 0 or (self.floating_disk and self.towers[row][real_tower] == self.floating_disk[0]):
          continue
        line = self.towers[row][real_tower]
        if isinstance(line[0], tuple):
          line = line[0]
        w = line[0]
        color = line[1]
        x = x0 + display_tower * STEP - w / 2
        y = y0 - DISK_HEIGHT * (row + 1)
        self.canvas.create_rectangle(x, y, x + w, y + DISK_HEIGHT, outline=color, fill=color)
        self.canvas.create_text(x + w / 2, y + DISK_HEIGHT / 2, text=str(w), fill=SHOW_LABEL, font=("Courier", 10, "bold"))

    self.canvas.pack(fill=BOTH, expand=1)
    if self.floating_disk:
      self.draw_floating_disk(self.floating_disk)

  def draw_base(self):
      color = "#ffffff"
      H = RINGS * DISK_HEIGHT
      x1 = x0+STEP*8
      y1 = y0+10

      self.canvas.create_rectangle(x0-70, y0, x1-70, y1, outline="#0bf", fill=color)
      self.canvas.pack(fill=BOTH, expand=1)
      for i in range(8):
        x1 = int(x0 - 3 + i * STEP)
        y1 = int(y0 - H)
        x2 = x1 + 6
        y2 = y0
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="#0bf", fill=color)
        self.canvas.pack(fill=BOTH, expand=1)

  def draw_iteration(self, percent):
    self.floating_disk = ()
    target_iteration = percent / 100 * self.total_iterations
    self.towers = deepcopy(self.initial_towers)
    is_float = False

    if '.' in str(target_iteration):
      before_comma, after_comma = str(target_iteration).split('.')
      if int(after_comma) == 0:
        target_iteration = int(before_comma)
        target_iteration_int = int(before_comma)
      else:
        target_iteration_int = int(before_comma)
        target_iteration = float(before_comma + '.' + after_comma[:3])
        is_float = True

    self.current_iteration_label.config(text=f"Текущая итерация {target_iteration}")

    if is_float:
      self.process_iterations(target_iteration_int - 1)
    else:
      self.process_iterations(target_iteration_int)

    if is_float:
      disk, from_, old_row, to_, new_row = self.iterations_log[target_iteration_int] # (diameter, color), tower_index, row_index, tower_index, row_index
      self.floating_disk = (disk, from_, old_row, to_)

    self.draw_towers()

  def process_iterations(self, target_iteration):
    if target_iteration < 1: return
    self.towers = deepcopy(self.initial_towers)

    for iteration in self.iterations_log[:target_iteration]:
      disk, from_, old_row, to_, new_row = iteration # (diameter, color), tower_index, row_index, tower_index, row_index
      self.towers[old_row][from_] = (0, "#000000")
      self.towers[new_row][to_] = disk
      

  def draw_end(self):
    self.draw_iteration(100)

  def draw_floating_disk(self, data):
    disk, from_, old_row, to_ = data
    self.towers[old_row][from_] = (0, '#000000')
    w = disk[0]
    color = disk[1]
    x_from = x0 + (7 - from_) * STEP
    x_to = x0 + (7 - to_) * STEP
    x = (x_from + x_to) / 2 - w / 2
    y = y0 - RINGS * DISK_HEIGHT - 30
    rectangle_id = self.canvas.create_rectangle(x, y, x + w, y + DISK_HEIGHT, outline=color, fill=color)
    text_id = self.canvas.create_text(x + w / 2, y + DISK_HEIGHT / 2, text=str(w), fill=SHOW_LABEL, font=("Courier", 10, "bold"))
    self.canvas.tag_raise(rectangle_id)
    self.canvas.tag_raise(text_id)

  def find_tower(self, disk):
    for tower in range(8):
      for row in range(72):
        if self.towers[row][tower][0] == disk[0][0]:
          return tower
    return None

  def can_place_on_top(self, diameter, target_tower):
    for row in range(72):
      if self.towers[row][target_tower][0] == 0:
        if row == 0:
          return True
        below_disk = self.towers[row - 1][target_tower]
        return below_disk[0] < diameter
    return False
  
  def move_disk_to_first_tower(self, disk):
    disk_data = disk[0]
    row = disk[1]
    tower = disk[2]

    n = 1
    if tower == 7:
      n = 2

    # выйти с рекурсии если диск на первой башне
    if tower == 0: return

    if self.can_place_on_top(disk_data[0], tower - n):
      available_place = self.find_top_available_place(tower - n)
      if available_place >= 0:
        self.towers[row][tower] = (0, '#000000')
        
        self.towers[available_place][tower - n] = disk_data
        self.iterations_log.append((disk_data, tower, row, tower-n, available_place))
        self.total += 1

        self.move_disk_to_first_tower([disk_data, available_place, tower - n])
        
  def change_disk_data(self, new_disk_data):
    disk_data = new_disk_data[0]

    for disk in self.disks:
      if disk[0][0] == disk_data[0]:
        disk = new_disk_data

  def find_top_available_place(self, tower_index):
    for row in range(72):
      if self.towers[row][tower_index][0] == 0:
        return row
    return False

  def calculate_total_iterations(self):
    self.iterations_log = []
    self.total = 0
    for disk in self.disks:
      if disk[0][0] < 20: continue
      self.move_disk_to_first_tower(disk)

    return len(self.iterations_log)

  def draw_pos1(self):
    p = int(self.input_pos1.get("1.0", "end").replace("\n", ""))
    self.draw_iteration(p)
  
  def draw_pos2(self):
    p = int(self.input_pos2.get("1.0", "end").replace("\n", ""))
    self.draw_iteration(p)

  def draw_pos3(self):
    p = int(self.input_pos3.get("1.0", "end").replace("\n", ""))
    self.draw_iteration(p)

  def draw_pos4(self):
    p = int(self.input_pos4.get("1.0", "end").replace("\n", ""))
    self.draw_iteration(p)

if __name__ == '__main__':
  root = tk.Tk()
  app = App()
  w = STEP * 10 + 30
  h = RINGS * DISK_HEIGHT + 20 + 200
  root.geometry(f"{w}x{h}")
  root.mainloop()