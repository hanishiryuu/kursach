import tkinter as tk

from tkinter import Frame, Text, Button

class App:
  def __init__(self, root):
    # Инициализация рута и клиентов
    self.root = root
    self.root.title('Банковская система')
    self.clients = { 'Lavrentev': 70194603 } # { name: balance }

    # Страница
    page = Frame(root)
    page.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Левая сторона страницы
    page_left = Frame(page)
    page_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    self.input_label = tk.Label(page_left, text='Введите команды (макс. 20):')
    self.input_label.pack()
    
    # Инпут для входных данных
    self.input = Text(page_left, width=40, height=20)
    self.input.pack(fill=tk.BOTH, expand=True)

    # Правая сторона страницы
    page_right = Frame(page)
    page_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    self.output_label = tk.Label(page_right, text='Вывод')
    self.output_label.pack()

    # Инпут для показа данных
    self.output = Text(page_right, width=40, height=20)
    self.output.pack(fill=tk.BOTH, expand=True)

    page_top = Frame(page)
    page_top.pack(side=tk.TOP, fill=tk.BOTH, pady=20)

    # Кнопки
    # Calculate
    self.button_calculate = Button(page_top, text='Calculate', command=self.calculate)
    self.button_calculate.pack()

    # Clear
    self.button_clear = Button(page_top, text='Clear', command=self.clear)
    self.button_clear.pack()

  def calculate(self):
    commands = self.input.get('1.0', tk.END).strip().split('\n')
    self.clearOutput()

    for command in commands: 
      if not command.strip():
        continue

      parts = command.strip().split()
      operation = parts[0]
      operands = parts[1:]

      match operation:
        case 'DEPOSIT':
          if len(operands) < 2:
            self.output.insert(tk.END, f'Недостаточно параметров\n')
            return

          name, sum = operands[0], float(operands[1])
          self.clients[name] = self.clients.get(name, 0) + sum
          self.output.insert(tk.END, f'Депозит: {name} на сумму {sum:.10g}уе\n')

        case 'WITHDRAW':
          if len(operands) < 2:
            self.output.insert(tk.END, f'Недостаточно параметров\n')
            return

          name, sum = operands[0], float(operands[1])
          self.clients[name] = self.clients.get(name, 0) - sum
          self.output.insert(tk.END, f'Снятие: {name} на сумму {sum:.10g}уе\n')

        case 'BALANCE':
          if len(operands) == 0:
            for name, balance in self.clients.items():
              self.output.insert(tk.END, f'{name} {balance:.10g}уе\n')
          else:
            name = operands[0]
            balance = self.clients.get(name, 'NO CLIENT')

            if balance == 'NO CLIENT':
              self.output.insert(tk.END, f'{name} {balance:.10g}\n')
            else:
              self.output.insert(tk.END, f'{name} {balance:.10g}уе\n')
          
        case 'TRANSFER':
          if len(operands) < 3:
            self.output.insert(tk.END, f'Недостаточно параметров\n')
            return

          client_from, client_to, sum = operands[0], operands[1], float(operands[2])
          self.clients[client_from] = self.clients.get(name, 0) - sum
          self.clients[client_to] = self.clients.get(name, 0) + sum
          self.output.insert(tk.END, f'Перевод: От {client_from} к {client_to} на сумму {sum:.10g}уе\n')

        case 'INCOME':
          if len(operands) == 0:
            self.output.insert(tk.END, f'Недостаточно параметров\n')
            return
          p = float(operands[0])
          for name, balance in self.clients.items():
            is_balance_negative = balance < 0
            if is_balance_negative:
              balance = -balance
              
            new_balance = balance * ( p / 100 )

            if is_balance_negative:
              new_balance = -new_balance
            
            self.clients[name] += new_balance
          self.output.insert(tk.END, f'Начислено: {p:.10g}% от суммы остатка всем клиентам\n')

        case _:
          if operation.upper() in ['DEPOSIT', 'WITHDRAW', 'BALANCE', 'TRANSFER', 'INCOME']:
            self.output.insert(tk.END, f'Команда введена неверно: {operation}\n')
          else:
            self.output.insert(tk.END, f'Неизвестная команда: {operation}\n')
          return
          
  def clearInput(self):
    self.input.delete('1.0', tk.END)
    
  def clearOutput(self):
    self.output.delete('1.0', tk.END)
    
  def clear(self):
    self.clearInput()
    self.clearOutput()

if __name__ == '__main__':
  root = tk.Tk()
  app = App(root)
  root.mainloop()