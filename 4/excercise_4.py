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
    self.towers_top_disks = {} # tower_index: disk_diameter

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
    self.calculate_total_iterations()
    self.flag = False
 
  def get_initial_state(self):
    text = self.input_id.get("1.0", "end").replace("\n", "")
    if len(text) == 8 and text.isdigit():
        self.student_id = text
    self.init_towers(update_existing=False)
    self.draw_towers()







  def init_towers(self, update_existing=True):
    # self.towers = [[(0, "#000000") for _ in range(8)] for _ in range(72)]
    # for tower in range(8):
    #   is_added = False
    #   for row in range(int(self.student_id[tower])):
    #     m = tower + 1
    #     n = int(self.student_id[tower]) - row
    #     if make_colors:
    #       color = f"#{random.randint(100000, 999999)}"
    #     self.towers[row][tower] = (m * 10 + n, color)
    #     self.disks.append([self.towers[row][tower][0], self.towers[row][tower][0], row, tower]) # diameter, color, row, tower

    #     if row == int(self.student_id[tower]) - 1:
    #       self.towers_top_disks[tower] = self.towers[row][tower][0]
    #       is_added = True

    #   if not is_added:
    #     self.towers_top_disks[tower] = 0

    # self.initial_towers = self.towers.copy()
    # self.disks = sorted(self.disks, key=lambda x: x[0])
    # self.total_disks = len(self.disks)
    self.towers = {peg: [] for peg in range(8)}
    self.towers_to_draw = [[(0, "#000000") for _ in range(8)] for _ in range(72)]
    for index, digit in enumerate(self.student_id):
      peg = 7 - index
      n = int(digit)
      if n > 0:
        disks = [((peg + 1) * 10 + nn, f"#{random.randint(100000, 999999)}") for nn in range(1, n+1)]
        self.disks.extend(disks)
        self.towers[index] = sorted(disks, key=lambda x: x[0], reverse=True)
    for tower in range(8):
      for index, disk in enumerate(reversed(self.towers[tower])):
        diameter, color = disk
        row = len(self.towers[tower]) - index - 1
        self.towers_to_draw[row][tower] = (diameter, color)
    self.initial_towers = [disk for row in self.towers_to_draw for disk in row if disk[0] != 0]
  

  def draw_towers(self):
    self.canvas.delete("all")
    self.draw_base()
    for display_tower in range(8):
      real_tower = display_tower
      for disk_index in range(len(self.towers[real_tower])):
        if self.towers[real_tower][0] == 0:
          self.list_labels[disk_index][display_tower].config(text="0")
          self.list_labels[disk_index][display_tower].config(fg=self.master["bg"])
          self.list_labels[disk_index][display_tower].config(state='normal')
          continue
        disk = self.towers_to_draw[disk_index][real_tower]
        w = disk[0]
        color = disk[1]
        x = x0 + display_tower * STEP - w / 2
        y = y0 - HEIGHT * (disk_index + 1)
        self.canvas.create_rectangle(x, y, x + w, y + HEIGHT, outline=color, fill=color)
        self.list_labels[disk_index][display_tower].config(text=str(w))
        self.list_labels[disk_index][display_tower].config(fg=SHOW_LABEL)
        self.list_labels[disk_index][display_tower].config(state='normal')
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
    self.towers_to_draw = self.initial_towers.copy()

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
    self.towers_to_draw = self.initial_towers.copy()

    for iteration in self.iterations_log[:target_iteration]:
      disk, from_, to_ = iteration
      print(iteration, self.towers_to_draw)
      if 0 <= from_ < 8 and 0 <= to_ < 8:
        for row in range(72):
          if self.towers_to_draw[row][from_] == disk:
            self.towers_to_draw[row][from_] = (0, "#000000")
            break
        for row in range(72):
          if self.towers_to_draw[row][to_] == (0, "#000000"):
            self.towers_to_draw[row][to_] = disk
            break

  def draw_end(self):
    self.towers_to_draw = [[(0, "#000000") for _ in range(8)] for _ in range(72)]
    for i, disk in enumerate(self.disks):
        self.towers_to_draw[i][0] = disk
    self.draw_towers()

  def draw_floating_disk(self, disk, from_, to_):
    w = disk[0]
    color = disk[1]
    x_from = x0 + (7 - from_) * STEP
    x_to = x0 + (7 - to_) * STEP
    x = (x_from + x_to) / 2 - w / 2
    y = y0 - RINGS * HEIGHT - 30
    self.canvas.create_rectangle(x, y, x + w, y + HEIGHT, outline=color, fill=color)







  def move_top_disk(self, src, dst):
    disk = self.towers[src].pop()        # remove top disk from source
    self.towers[dst].append(disk)        # place it on destination

    for row in range(72):
      if self.towers_to_draw[row][src-1][0] == disk[0]:
        self.towers_to_draw[row][src-1] = (0, "#000000")
        break
    for row in range(72):
      if self.towers_to_draw[row][dst-1][0] == 0:
        self.towers_to_draw[row][dst-1] = disk
        break
        
    self.log_iteration(disk, src, dst)

  def log_iteration(self, disk, from_, to_):
    self.current_iteration += 1
    self.iterations_log.append((disk, from_, to_))
    # print(f"перемещен диск {disk} с башни {7 - from_} на башню {7 - to_}")

  def free_top(self, peg, max_diameter, exclude=None):
      if exclude is None:
          exclude = set()
      # If peg is empty or top disk is smaller than the moving disk, it's free
      if not self.towers[peg] or self.towers[peg][-1] < max_diameter:
          return
      # Otherwise, move the smaller top disk out of the way
      top_small = self.towers[peg][-1]
      for neighbor in allowed_transitions[peg]:
          if neighbor == 1 or neighbor in exclude:
              continue
          if not self.towers[neighbor] or self.towers[neighbor][-1] < top_small:
              self.free_top(neighbor, top_small, exclude | {peg})
              self.move_top_disk(peg, neighbor)
              self.free_top(peg, max_diameter, exclude)
              return
      # As a fallback, allow moving into any other neighbor
      for neighbor in allowed_transitions[peg]:
          if neighbor in exclude:
              continue
          if not self.towers[neighbor] or self.towers[neighbor][-1] < top_small:
              self.free_top(neighbor, top_small, exclude | {peg})
              self.move_top_disk(peg, neighbor)
              self.free_top(peg, max_diameter, exclude)
              return

  def move_to_target(self, d):
      # Find which tower currently holds disk d
      src = next(peg for peg, stack in self.towers.items() if d in stack)
      if src == 1:
          return
      # Find path from src to target (1) using BFS
      parents = {src: None}
      queue = deque([src])
      while queue:
          peg = queue.popleft()
          if peg == 1:
            break
          for neigh in allowed_transitions[peg]:
            if neigh not in parents:
              parents[neigh] = peg
              queue.append(neigh)
      # Reconstruct the path
      path = []
      peg = 1
      while peg is not None:
          path.append(peg)
          peg = parents[peg]
      path.reverse()  # now [src, ..., 1]
      # Move disk along the path
      for i in range(len(path) - 1):
          cur = path[i]
          nxt = path[i+1]
          # Ensure target peg is free for this disk
          self.free_top(nxt, d, exclude={cur})
          self.move_top_disk(cur, nxt)


  def can_place_on_top(self, disk, tower_index):
    disk_diameter = disk[0] if isinstance(disk, tuple) else disk
    
    target_tower_top_disk_diameter = 0
    target_tower_top_disk_diameter = self.towers_top_disks[tower_index]
    if target_tower_top_disk_diameter < disk_diameter:
      return True
    return False

  def calculate_total_iterations(self):
    # Reset logs and counters
    self.iterations_log = []
    self.current_iteration = 0
    # Initialize towers without colors for pure logic
    self.init_towers(update_existing=True)

    self.towers_to_draw = [[(0, "#000000") for _ in range(8)] for _ in range(72)]
    for peg, stack in self.towers.items():
        for i, disk in enumerate(reversed(stack)):
            self.towers_to_draw[i][peg] = disk
    
    # Gather all disks sorted from largest to smallest
    all_disks = sorted([d for stack in self.towers.values() for d in stack], reverse=True)
    # Move each disk in turn to Tower 1
    for disk in all_disks:
      # Free any smaller disks blocking the disk on its current tower
      current_peg = next((peg for peg, stack in self.towers.items() if disk in stack), None)
      if current_peg is None or current_peg == 0:
        continue
      if self.towers[current_peg][-1] != disk:
        self.free_top(current_peg, disk)
      # Move the disk along allowed transitions to Tower 1
      self.move_to_target(disk)
    # Record total iterations
    self.total_iterations = self.current_iteration
    print(f"Всего шагов: {self.total_iterations}")
    self.initial_towers = {k: list(v) for k, v in self.towers.items()}









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