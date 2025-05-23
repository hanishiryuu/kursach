import tkinter as tk
from tkinter import Frame, Button
import math

class CalculatorLogic:
  def __init__(self, student_id):
    self.student_id = student_id
    self.history = []
    self.operation = ''
    self.current_input = ''
    self.previous_input = ''


  def make_int_if_zero(self, number):
    if '.' in str(number):
      before_comma, after_comma = str(number).split('.')
      if all(d == '0' for d in after_comma):
        return int(before_comma)
    else:
      return int(number)

    return float(number)

  def calculate_display_lines(self):
    lines = sum(int(digit) for digit in str(self.student_id))

    while lines > 9:
      lines = sum(int(digit) for digit in str(lines))

    return max(2, lines)

  def calculate_memory_cells(self):
    cells = sum(int(digit) for digit in str(self.student_id)[-3:])

    while cells > 9:
      cells = sum(int(digit) for digit in str(cells))

    cells = max(2, cells)
    self.memory = [0] * cells
    
    return cells
  
  def handle_clear(self):
    self.current_input = ''
    self.operation = ''
    self.history = []

  def handle_operation(self, operation: str):
    if self.current_input == '': return

    self.previous_input = self.current_input
    self.operation = operation
    self.history.extend([self.current_input, operation])
    self.current_input = ''
  
  def handle_decimal(self):
    if self.current_input == '' or '.' in self.current_input: return
      
    self.current_input += '.'

  def handle_power(self, power):
    if self.current_input == '': return
    result = float(self.current_input) ** power

    if '.' in str(result):
      before_comma, after_comma = str(result).split('.')
      if all(d == '0' for d in after_comma):
        result = int(before_comma)

    self.history.extend([self.current_input, f'pow{power}'])
    self.current_input = str(result)

  def handle_sqrt(self):
    if self.current_input == '': return

    if float(self.current_input) < 0:
      self.history.append('Invalid operation!')
      return

    result = math.sqrt(float(self.current_input))

    result = self.make_int_if_zero(result)

    self.history.extend([self.current_input, 'sqrt'])
    self.current_input = str(result)

  def handle_invert(self):
    if self.current_input == '': return

    if self.current_input[0] == '-':
      self.current_input = self.current_input[1:]
    else:
      self.current_input = '-' + self.current_input

  def handle_equals(self):
    if self.current_input == '' or self.previous_input == '' or not self.operation: return

    x = float(self.previous_input)
    y = float(self.current_input)
    result = None

    self.history.extend([self.current_input, '='])

    match (self.operation):
      case '+':
        result = x + y
      case '-':
        result = x - y
      case '*':
        result = x * y
      case '%':
        result = x % y
      case '/':
        if y == 0:
          self.history.append('Invalid operation!')
          return
        result = x / y
      case 'x^y':
        result = x ** y

    self.operation = ''
    result = self.make_int_if_zero(result)
    self.current_input = str(result)
    
  def handle_reciprocal(self):
    if self.current_input == '': return
    
    x = float(self.current_input)

    if x == 0:
      self.history.append('Invalid operation!')
      return
    
    result = 1 / x

    result = self.make_int_if_zero(result)

    self.current_input = str(result)

  def handle_student_id_change(self, new_id):
    new_id = new_id.strip()   

    if len(new_id) < 3 or not new_id.isdigit(): return

    self.student_id = new_id
  
  def handle_asin(self):
    if self.current_input == '': return
    
    x = float(self.current_input)
    
    if x < -1 or x > 1:
        self.history.append('Invalid input for asin!')
        return
    
    result = math.asin(x)
    result = math.degrees(result)
    
    result = self.make_int_if_zero(result)
    
    self.history.extend([self.current_input, 'asin'])
    self.current_input = str(result)

  def handle_acos(self):
    if self.current_input == '': return
    
    x = float(self.current_input)
    
    if x < -1 or x > 1:
        self.history.append('Invalid input for acos!')
        return
    
    result = math.acos(x)
    result = math.degrees(result)
    
    result = self.make_int_if_zero(result)
    
    self.history.extend([self.current_input, 'acos'])
    self.current_input = str(result)

  def handle_memory_add(self, cell):
    number = self.make_int_if_zero(self.current_input)
    
    memory = self.make_int_if_zero(self.memory[cell])
    
    self.memory[cell] = memory + number 

    self.history.append(f'M+{self.current_input} = {self.memory[cell]}')
    
  def handle_memory_subtract(self, cell):
    number = self.make_int_if_zero(self.current_input)
    
    memory = self.make_int_if_zero(self.memory[cell])
    
    self.memory[cell] = memory - number 

    self.history.append(f'M-{self.current_input} = {self.memory[cell]}')

  def handle_memory_store(self, cell):
    self.memory[cell] = self.current_input
    self.history.append(f'Stored {self.memory[cell]}')

  def handle_memory_clear(self, cell):
    self.memory[cell] = 0
    self.history.append('Cleared')

  def handle_memory_recall(self, cell):
    self.current_input = self.memory[cell]



class CalculatorInterface:
  def __init__(self, root, student_id):
    self.root = root
    self.root.title('Калькулятор')
    self.is_advanced_mode = False
    self.logic = CalculatorLogic(student_id)
    self.memory_cells = self.logic.calculate_memory_cells()

    # Правая сторона страницы
    self.page_right = Frame(self.root)
    self.page_right.pack(side=tk.RIGHT, pady=10)

    # Левая сторона страницы
    self.page_calc = Frame(self.root)
    self.page_calc.pack(side=tk.LEFT, pady=10)

    # дисплей
    self.display_wrapper = Frame(self.page_calc, padx=3, pady=3)
    self.display_wrapper.pack()

    self.mount_history_display()

    self.display = tk.Text(self.display_wrapper, height=1, width=50, state="disabled")
    self.display.pack(side=tk.BOTTOM, fill=tk.BOTH)

    # обычные кнопки
    self.buttons_wrapper = Frame(self.page_calc)
    self.buttons_wrapper.pack(padx=10)

    # (text, row, column, function)
    self.buttons = [
      ('≡',   0, 0,   self.toggle_advanced_mode),
      ('< >', 0, 1,   self.handle_student_id_change_click),
      ('C',   0, 4,   self.handle_clear_click),
      ('%',   1, 0,   lambda: self.handle_operation_click('%')),
      ('<-',  1, 1,   self.handle_backspace_click),
      ('1/x', 1, 2,   self.handle_reciprocal_click),
      ('x²',  1, 3,   self.handle_square_click),
      ('CE',  1, 4,   self.handle_clear_current_click),
      ('7',   2, 0,   self.handle_digit_click), 
      ('8',   2, 1,   self.handle_digit_click),
      ('9',   2, 2,   self.handle_digit_click),
      ('/',   2, 3,   lambda: self.handle_operation_click('/')),
      ('x^y', 2, 4,   lambda: self.handle_operation_click('x^y')),
      ('4',   3, 0,   self.handle_digit_click),
      ('5',   3, 1,   self.handle_digit_click),
      ('6',   3, 2,   self.handle_digit_click),
      ('*',   3, 3,   lambda: self.handle_operation_click('*')),
      ('√',   3, 4,   self.handle_sqrt_click),
      ('1',   4, 0,   self.handle_digit_click),
      ('2',   4, 1,   self.handle_digit_click),
      ('3',   4, 2,   self.handle_digit_click),
      ('-',   4, 3,   lambda: self.handle_operation_click('-')),
      ('+/-', 4, 4,   self.handle_invert_click),
      ('0',   5, 0,   self.handle_digit_click),
      ('.',   5, 2,   self.handle_decimal_click),
      ('+',   5, 3,   lambda: self.handle_operation_click('+')), 
      ('=',   5, 4,   self.handle_equals_click)
    ]
  
    for (text, row, column, func) in self.buttons:
      if text.isdigit():
        button = Button(self.buttons_wrapper, text=text, width=4,
                        command=lambda t=text: self.handle_digit_click(t))
      else:
        button = Button(self.buttons_wrapper, text=text, width=3, command=func)

      button.grid(row=row, column=column, columnspan=2 if text == '0' else 1, padx=2, pady=2, sticky="nsew")


  # Маунт дисплея истории
  def mount_history_display(self):
    self.history_display_lines = self.logic.calculate_display_lines()

    self.history_display = tk.Text(self.display_wrapper, height=self.history_display_lines, width=50, state="disabled")
    self.history_display.pack(side=tk.TOP, fill=tk.BOTH)

  def unmount_history_display(self):
    if hasattr(self, 'history_display'):
      self.history_display.pack_forget()

  def update_history_display_height(self):
    self.unmount_history_display()
    self.mount_history_display()

  # Ячейки памяти
  def mount_memory_section(self):
    self.page_memory = Frame(self.page_right)
    self.page_memory.pack(side=tk.BOTTOM)
    self.memory_buttons_wrapper = Frame(self.page_memory)
    self.memory_buttons_wrapper.pack(side=tk.BOTTOM, padx=10, pady=10)

    memory_title = tk.Label(self.page_memory, text='Управление памятью')
    memory_title.pack(side=tk.TOP, pady=(10, 0))

    # ряды кнопок 
    for i in range(self.memory_cells):
      label = tk.Label(self.memory_buttons_wrapper, text=i + 1)
      label.grid(row=i, column=0)

      tk.Button(self.memory_buttons_wrapper, text="MC", command=lambda index=i: self.handle_memory_clear_click(index)).grid(row=i, column=1, padx=2, pady=2, sticky="nsew")
      tk.Button(self.memory_buttons_wrapper, text="MR", command=lambda index=i: self.handle_memory_recall_click(index)).grid(row=i, column=2, padx=2, pady=2, sticky="nsew")
      tk.Button(self.memory_buttons_wrapper, text="MS", command=lambda index=i: self.handle_memory_store_click(index)).grid(row=i, column=3, padx=2, pady=2, sticky="nsew")
      tk.Button(self.memory_buttons_wrapper, text="M+", command=lambda index=i: self.handle_memory_add_click(index)).grid(row=i, column=4, padx=2, pady=2, sticky="nsew")
      tk.Button(self.memory_buttons_wrapper, text="M-", command=lambda index=i: self.handle_memory_subtract_click(index)).grid(row=i, column=5, padx=2, pady=2, sticky="nsew")


  # обновление UI 
  def unmount_memory_section(self):
    if hasattr(self, 'page_memory'): 
      self.page_memory.pack_forget()

  def update_memory_section(self):
    self.unmount_memory_section()
    self.mount_memory_section()

  def mount_advanced_section(self):
    self.page_advanced = Frame(self.page_right)
    self.page_advanced.pack(side=tk.TOP)

    # Блок изменения айди
    self.student_id_wrapper = Frame(self.page_advanced)
    self.student_id_wrapper.pack()

    student_id_title = tk.Label(self.student_id_wrapper, text='Лаврентьев Егор Николаевич')
    student_id_title.pack(side=tk.TOP, pady=(10, 0))

    self.student_id_input = tk.Text(self.student_id_wrapper, width=40, height=1)
    self.student_id_input.pack(fill=tk.X)

    # кнопка подтверждения изменения айди
    self.student_id_button = tk.Button(self.student_id_wrapper, text='Confirm', command=self.handle_student_id_change_click)
    self.student_id_button.pack()

    self.student_id_input.insert('1.0', self.logic.student_id)

    # Кнопки расширенного режима
    self.advanced_buttons_wrapper = Frame(self.page_advanced)
    self.advanced_buttons_wrapper.pack(side=tk.BOTTOM, padx=10, pady=10)

    advanced_title = tk.Label(self.page_advanced, text='Дополнительные функции')
    advanced_title.pack(side=tk.BOTTOM, pady=(10, 0))

    self.advanced_buttons = [
      ('x³',   0, self.handle_cube_click),
      ('asin', 1, self.handle_asin_click),
      ('acos', 2, self.handle_acos_click),
    ]

    for (text, column, func) in self.advanced_buttons:
      button = Button(self.advanced_buttons_wrapper, text=text, width=3, command=func)

      button.grid(row=1, column=column, padx=2, pady=2, sticky="nsew")

  def unmount_advanced_section(self):
    if hasattr(self, 'page_advanced'): 
      self.page_advanced.pack_forget()

  def update_display(self):
    self.display.config(state="normal")
    self.display.delete('1.0', tk.END)
    self.display.insert('1.0', self.logic.current_input)
    self.display.config(state="disabled")

  def update_history_display(self):
    self.history_display.config(state='normal')
    self.history_display.delete(1.0, tk.END)

    if len(self.logic.history) < self.history_display_lines:
      for i in range(self.history_display_lines - len(self.logic.history)):
        self.history_display.insert('1.0', '\n')

    for item in self.logic.history[-self.history_display_lines:]:
      self.history_display.insert(tk.END, item + '\n')

    self.history_display.config(state='disabled')

  # Перевод инпутов юзера в логику
  def update_displays(self):
    self.update_display()
    self.update_history_display()

  def handle_operation_click(self, operation: str):
    self.logic.handle_operation(operation)
    self.update_displays()
  
  def handle_digit_click(self, digit):
    self.logic.current_input += str(digit)
    self.update_display()

  def handle_decimal_click(self):
    self.logic.handle_decimal()
    self.update_display()
    
  def handle_clear_click(self):
    self.logic.handle_clear()
    self.update_displays()

  def handle_clear_current_click(self):
    self.logic.current_input = ''
    self.update_display()

  def handle_backspace_click(self):
    self.logic.current_input = self.logic.current_input[:-1]
    self.update_display()

  def handle_square_click(self):
    self.logic.handle_power(2)
    self.update_displays()

  def handle_equals_click(self):
    self.logic.handle_equals()
    self.update_displays()

  def handle_sqrt_click(self):
    self.logic.handle_sqrt()
    self.update_displays()

  def handle_reciprocal_click(self):
    self.logic.handle_reciprocal()
    self.update_displays()

  def handle_cube_click(self):
    self.logic.handle_power(3)
    self.update_displays()

  def handle_sin_click(self):
    self.logic.handle_sin()
    self.update_displays()

  def handle_asin_click(self):
    self.logic.handle_asin()
    self.update_displays()

  def handle_acos_click(self):
    self.logic.handle_acos()
    self.update_displays()

  def handle_invert_click(self):
    self.logic.handle_invert()
    self.update_display()

  # Memory
  def handle_memory_add_click(self, cell):
    self.logic.handle_memory_add(cell)
    self.update_history_display()

  def handle_memory_subtract_click(self, cell):
    self.logic.handle_memory_subtract(cell)
    self.update_history_display()

  def handle_memory_store_click(self, cell):
    self.logic.handle_memory_store(cell)
    self.update_history_display()

  def handle_memory_recall_click(self, cell):
    self.logic.handle_memory_recall(cell)
    self.update_display()

  def handle_memory_clear_click(self, cell):
    self.logic.handle_memory_clear(cell)
    self.update_history_display()

  def toggle_advanced_mode(self):
    if self.is_advanced_mode == True:
      self.root.title('Калькулятор – расширенный режим')
      self.unmount_memory_section()
      self.unmount_advanced_section()
      self.page_right.pack_forget()
      self.is_advanced_mode = False
    else:
      self.root.title('Калькулятор')
      self.page_right.pack()
      self.mount_memory_section()
      self.mount_advanced_section()
      self.is_advanced_mode = True

  def handle_student_id_change_click(self):
    new_id = self.student_id_input.get('1.0', tk.END)
    self.logic.handle_student_id_change(new_id)
    self.memory_cells = self.logic.calculate_memory_cells()

    self.update_history_display_height()
    self.update_memory_section()


if __name__ == '__main__':
  student_id = 70194603
  root = tk.Tk()
  app = CalculatorInterface(root, student_id)
  root.mainloop()
  