import tkinter as tk
import random


class Logic:
    def __init__(self, student_id):
        self.student_id = str(student_id)
        self.spindle_count = 8
        self.spindles = [[] for _ in range(self.spindle_count)]
        self.all_disks = []
        self.total_iterations = 0
        self.build_initial_state()

    def build_initial_state(self):
        for spindle_index, digit_char in enumerate(reversed(self.student_id)):
            disk_count = int(digit_char)
            for disk_position in range(disk_count):
                diameter = (spindle_index + 1) * 10 + disk_position
                self.spindles[spindle_index].append(diameter)
                self.all_disks.append(diameter)

    def get_initial_state(self):
        return [list(spindle) for spindle in self.spindles]

    def get_final_state(self):
        final_spindles = [[] for _ in range(self.spindle_count)]
        sorted_disks = sorted(self.all_disks)
        final_spindles[0] = sorted_disks
        return final_spindles

    def get_iteration_state(self, iteration_number):
        if iteration_number == 0:
            return self.get_initial_state()
        elif iteration_number >= 1.0:
            return self.get_final_state()
        else:
            partial_spindles = [list(spindle) for spindle in self.spindles]
            floating_disk = sorted(self.all_disks, reverse=True)[int(len(self.all_disks) * iteration_number)]
            return partial_spindles, floating_disk


class App:
    def __init__(self, root, logic_class, width=1200, height=800):
        self.root = root
        self.root.title("Модифицированная задача о Ханойских башнях")
        self.window = root
        self.logic = logic_class
        self.canvas_width = width
        self.canvas_height = height
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()
        self.disk_colors = {}
        self.disk_height = 12
        self.spindle_spacing = 120
        self.spindle_base_y = 600
        self.spindle_top_y = 200
        self.status_label = tk.Label(root, text="Итерация 0", font=('Arial', 14))
        self.status_label.pack()

        self.build_ui()

    def build_ui(self):
        button_frame = tk.Frame(self.window)
        button_frame.pack()

        tk.Button(button_frame, text="Начало", command=lambda: self.display_state(0)).grid(row=0, column=0)

        self.percent_entries = []
        for i in range(4):
            percent_value = int(self.logic.student_id[i * 2:i * 2 + 2])
            entry = tk.Entry(button_frame, width=5)
            entry.insert(0, str(percent_value))
            entry.grid(row=0, column=i + 2)
            self.percent_entries.append(entry)

            tk.Button(button_frame, text=f"Показать",
                      command=lambda i=i: self.display_percent(i)).grid(row=1, column=i + 2)

        tk.Button(button_frame, text="Окончание", command=lambda: self.display_state(1)).grid(row=0, column=1)
        
        self.display_state(0)

    def display_state(self, iteration):
        self.canvas.delete("all")
        if iteration == 0:
            spindles = self.logic.get_initial_state()
        elif iteration == 1:
            spindles = self.logic.get_final_state()
        else:
            spindles = self.logic.get_iteration_state(iteration)

        self.draw_spindles(spindles)
        self.status_label.config(text=f"Итерация {iteration}")

    def display_percent(self, index):
        percent = float(self.percent_entries[index].get())
        iteration_fraction = percent / 100
        self.display_state(iteration_fraction)

    def draw_spindles(self, spindles_data):
        for i in range(self.logic.spindle_count):
            spindle_x = (i + 1) * self.spindle_spacing
            self.canvas.create_line(spindle_x, self.spindle_top_y, spindle_x, self.spindle_base_y, width=4)

        if isinstance(spindles_data, tuple):
            spindles, floating_disk = spindles_data
        else:
            spindles = spindles_data
            floating_disk = None

        for i, spindle in enumerate(spindles):
            spindle_x = (i + 1) * self.spindle_spacing
            for j, diameter in enumerate(reversed(spindle)):
                self.draw_disk(diameter, spindle_x, self.spindle_base_y - j * self.disk_height)

        if floating_disk is not None:
            self.draw_disk(floating_disk, self.canvas_width // 2, self.spindle_top_y - 50, floating=True)

    def draw_disk(self, diameter, x_center, y_top, floating=False):
        if diameter not in self.disk_colors:
            self.disk_colors[diameter] = "#%06x" % random.randint(0, 0xFFFFFF)

        width = diameter
        color = self.disk_colors[diameter]
        self.canvas.create_rectangle(x_center - width // 2, y_top,
                                     x_center + width // 2, y_top + self.disk_height,
                                     fill=color, outline='black')
        self.canvas.create_text(x_center, y_top + self.disk_height // 2, text=str(diameter), fill='black')


if __name__ == '__main__':
    student_id = '70194603'
    logic = Logic(student_id)
    root = tk.Tk()
    app = App(root, logic)
    root.mainloop()