import tkinter as tk
from tkinter import Frame, Canvas, Text, Button, BOTH, Label
import random
from collections import deque

RINGS = 30
STEP = 130
HEIGHT = 10
x0 = 100
y0 = RINGS * HEIGHT + 50
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
    self.disks = []
    self.total_disks = 0
    self.total_iterations = 0
    self.current_iteration = 0
    self.iterations_log = []
    self.initial_disks = []

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
    y = HEIGHT + 440
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

    self.list_labels = list()
    max_item = 9
    for row in range(8*max_item):
      line = list()
      for tower in range(8):
        label = Label(self.master, text="0")
        x = x0 - STEP/2 + tower * STEP
        y = y0 - (row + 1) * HEIGHT
        label.config(font=("Courier", 7))
        label.place(x=x, y=y, width=10, height=7)
        label["fg"] = self.master["bg"]
        line.append(label)
      self.list_labels.append(line)

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

    self.initial_towers = self.towers.copy()
    self.disks = sorted(self.disks, key=lambda x: x[0])
    self.total_disks = len(self.disks)
      

  def draw_towers(self):
    self.canvas.delete("all")
    self.draw_base()
    for display_tower in range(8):
      real_tower = 7 - display_tower
      for row in range(RINGS):
        if self.towers[row][real_tower][0] == 0:
          self.list_labels[row][display_tower].config(text="0")
          self.list_labels[row][display_tower].config(fg=self.master["bg"])
          self.list_labels[row][display_tower].config(state='normal')
          continue
        line = self.towers[row][real_tower]
        if isinstance(line[0], tuple):
          line = line[0]
        w = line[0]
        color = line[1]
        x = x0 + display_tower * STEP - w / 2
        y = y0 - HEIGHT * (row + 1)
        self.canvas.create_rectangle(x, y, x + w, y + HEIGHT, outline=color, fill=color)
        self.list_labels[row][display_tower].config(text=str(w))
        self.list_labels[row][display_tower].config(fg=SHOW_LABEL)
        self.list_labels[row][display_tower].config(state='normal')
    self.canvas.pack(fill=BOTH, expand=1)

  def draw_base(self):
      color = "#ffffff"
      H = RINGS * HEIGHT
      x1 = x0+STEP*8
      y1 = y0+10

      self.canvas.create_rectangle(x0-70, y0, x1-70, y1, outline="#fb0", fill=color)
      self.canvas.pack(fill=BOTH, expand=1)
      for i in range(8):
        x1 = int(x0 - 3 + i * STEP)
        y1 = int(y0 - H)
        x2 = x1 + 6
        y2 = y0
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="#fb0", fill=color)
        self.canvas.pack(fill=BOTH, expand=1)

  def draw_iteration(self, percent):
    target_iteration = percent / 100 * self.total_iterations
    self.towers = self.initial_towers.copy()

    if '.' in str(target_iteration):
      before_comma, after_comma = str(target_iteration).split('.')
      if int(after_comma) == 0:
        target_iteration = int(before_comma)
        target_iteration_int = int(before_comma)
      else:
        target_iteration_int = int(before_comma)
        target_iteration = float(before_comma + '.' + after_comma[:3])

    self.current_iteration_label.config(text=f"Текущая итерация {target_iteration}")

    
    self.process_iterations(target_iteration_int)
    self.draw_towers()

  def process_iterations(self, target_iteration):
    self.towers = [[(0, "#000000") for _ in range(8)] for _ in range(72)]

    for iteration in self.iterations_log[:target_iteration]:
      disk, from_, to_ = iteration

      if self.can_place_on_top(disk, to_):
        for row in range(72):
          if self.towers[row][from_] == disk:
            self.towers[row][from_] = (0, "#000000")
            break
        for row in range(72):
          if self.towers[row][to_] == (0, "#000000"):
            self.towers[row][to_] = disk
            break


  def draw_end(self):
    self.towers = [[(0, "#000000") for _ in range(8)] for _ in range(72)]
    for i, disk in enumerate(self.disks):
        self.towers[i][0] = disk
    self.draw_towers()



  def draw_floating_disk(self, disk, from_, to_):
    w = disk[0]
    color = disk[1]
    x_from = x0 + (7 - from_) * STEP
    x_to = x0 + (7 - to_) * STEP
    x = (x_from + x_to) / 2 - w / 2
    y = y0 - RINGS * HEIGHT - 30
    self.canvas.create_rectangle(x, y, x + w, y + HEIGHT, outline=color, fill=color)

  def find_tower(self, disk):
    for tower in range(8):
      for row in range(72):
        if self.towers[row][tower][0] == disk[0][0]:
          return tower
    return None

  def can_place_on_top(self, disk, tower_index):
    for row in range(72):
      if self.towers[row][tower_index][0] == 0:
        if row == 0:
          return True
        below_disk = self.towers[row - 1][tower_index]
        return below_disk[0] > disk[0]
    return False

  def find_path_route(self, from_index, to_index, disk):
    from_peg = from_index + 1
    to_peg = to_index + 1

    max_steps = 500
    steps = 0
    visited = set()
    parent = {from_peg: None}
    queue = deque([from_peg])

    path_found = False

    while queue and steps < max_steps:
      steps += 1
      current = queue.popleft()
      if current == to_peg:
        path_found = True
        break
      for neighbor in allowed_transitions.get(current, []):
        if neighbor not in visited:
          if self.can_place_on_top(disk[0], neighbor - 1):
            visited.add(neighbor)
            parent[neighbor] = current
            queue.append(neighbor)

    if not path_found:
      return []

    path = []
    current = to_peg
    while current is not None:
      path.append(current - 1)
      current = parent.get(current)

    return path[::-1]

  def calculate_total_iterations(self):
    self.moves_log = []
    total = 0
    for disk in self.disks:
      print(f"Диск {disk} с башни {disk[2] + 1}")
      if disk[0] == 0:
          continue
      from_tower = disk[2]
      to_tower = 0
      if from_tower == to_tower:
          continue
      path = self.find_path_route(from_tower, to_tower, disk)
      if not path:
          print(f"⚠️ Нет допустимого пути для диска {disk} с башни {from_tower + 1} на башню {to_tower + 1}")
          continue
      for i in range(len(path) - 1):
          self.moves_log.append((disk, path[i], path[i + 1]))
      total += len(path) - 1
    print(f"✅ Всего найдено шагов: {total}")
    return total

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
  h = RINGS * HEIGHT + 20 + 200
  root.geometry(f"{w}x{h}")
  root.mainloop()