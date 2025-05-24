import tkinter as tk
import math
from tkinter import scrolledtext

class CalculatorLogic:
    def __init__(self, student_id):
        self.current_input = "0"
        self.previous_input = None
        self.current_operation = None
        self.reset_flag = False
        self.memory = [0] * self.calculate_memory_cells(student_id)
        self.history = []
        self.student_id = student_id
    
    def calculate_display_lines(self):
        num = sum(int(d) for d in str(self.student_id))
        while num > 9:
            num = sum(int(d) for d in str(num))
        return max(2, num)
    
    def calculate_memory_cells(self):
        last_three = str(self.student_id)[-3:]
        num = sum(int(d) for d in last_three)
        while num > 9:
            num = sum(int(d) for d in str(num))
        return max(2, num)
    
    def add_digit(self, digit):
        if self.reset_flag:
            self.current_input = "0"
            self.reset_flag = False
        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit
    
    def add_decimal_point(self):
        if "." not in self.current_input:
            self.current_input += "."
    
    def clear(self):
        self.current_input = "0"
        self.previous_input = None
        self.current_operation = None
    
    def set_operation(self, op):
        if self.current_operation and not self.reset_flag:
            self.calculate()
        self.previous_input = self.current_input
        self.current_operation = op
        self.reset_flag = True
    
    def calculate(self):
        if not self.previous_input or not self.current_operation:
            return

        try:
            a = float(self.previous_input)
            b = float(self.current_input)
            result = None

            if self.current_operation == "+":
                result = a + b
            elif self.current_operation == "-":
                result = a - b
            elif self.current_operation == "*":
                result = a * b
            elif self.current_operation == "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                result = a / b
            elif self.current_operation == "x^y":
                result = a ** b

            self.current_input = str(result)
            self.history.append(f"{self.previous_input} {self.current_operation} {b} = {result}")
            self.reset_flag = True

        except Exception as e:
            self.current_input = "Error"
            self.reset_flag = True
    
    def sqrt(self):
        try:
            num = float(self.current_input)
            if num < 0:
                raise ValueError("Negative number under root")
            self.current_input = str(math.sqrt(num))
            self.history.append(f"√({num}) = {self.current_input}")
            self.reset_flag = True
        except Exception as e:
            self.current_input = "Error"
            self.reset_flag = True
    
    def power(self, exponent=2):
        try:
            base = float(self.current_input)
            self.current_input = str(base ** exponent)
            self.history.append(f"{base}^{exponent} = {self.current_input}")
            self.reset_flag = True
        except Exception as e:
            self.current_input = "Error"
            self.reset_flag = True
    
    def cube(self):
        self.power(3)
    
    def sin(self):
        try:
            num = float(self.current_input)
            self.current_input = str(math.sin(num))
            self.history.append(f"sin({num}) = {self.current_input}")
            self.reset_flag = True
        except Exception as e:
            self.current_input = "Error"
            self.reset_flag = True
    
    def asin(self):
        try:
            num = float(self.current_input)
            if not -1 <= num <= 1:
                raise ValueError("Value out of domain")
            self.current_input = str(math.asin(num))
            self.history.append(f"asin({num}) = {self.current_input}")
            self.reset_flag = True
        except Exception as e:
            self.current_input = "Error"
            self.reset_flag = True
    
    def acos(self):
        try:
            num = float(self.current_input)
            if not -1 <= num <= 1:
                raise ValueError("Value out of domain")
            self.current_input = str(math.acos(num))
            self.history.append(f"acos({num}) = {self.current_input}")
            self.reset_flag = True
        except Exception as e:
            self.current_input = "Error"
            self.reset_flag = True
    
    def memory_add(self, cell=0):
        try:
            self.memory[cell] += float(self.current_input)
        except Exception as e:
            self.current_input = "Error"
    
    def memory_subtract(self, cell=0):
        try:
            self.memory[cell] -= float(self.current_input)
        except Exception as e:
            self.current_input = "Error"
    
    def memory_store(self, cell=0):
        try:
            self.memory[cell] = float(self.current_input)
        except Exception as e:
            self.current_input = "Error"
    
    def memory_recall(self, cell=0):
        self.current_input = str(self.memory[cell])
    
    def memory_clear(self, cell=0):
        self.memory[cell] = 0
    
    def change_sign(self):
        if self.current_input != "0":
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
    
    def inverse(self):
        try:
            num = float(self.current_input)
            if num == 0:
                raise ZeroDivisionError("Division by zero")
            self.current_input = str(1 / num)
            self.history.append(f"1/({num}) = {self.current_input}")
            self.reset_flag = True
        except Exception as e:
            self.current_input = "Error"
            self.reset_flag = True


class CalculatorApp:
    def __init__(self, root, student_id):
        self.root = root
        self.root.title("Calculator")
        self.logic = CalculatorLogic(student_id)
        self.advanced_mode = False
        self.create_ui()
    
    def create_ui(self):
        # Display area
        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(pady=5)
        
        self.display_lines = self.logic.calculate_display_lines()
        self.history_display = scrolledtext.ScrolledText(
            self.display_frame,
            height=self.display_lines,
            width=30,
            state='disabled',
            font=('Arial', 12)
        )
        self.history_display.pack()
        
        self.current_display = tk.Entry(
            self.display_frame,
            width=30,
            font=('Arial', 16),
            justify='right'
        )
        self.current_display.pack()
        self.current_display.insert(0, "0")
        
        # Button frames
        self.basic_frame = tk.Frame(self.root)
        self.advanced_frame = tk.Frame(self.root)
        self.basic_frame.pack()
        
        # Basic buttons
        basic_buttons = [
            ('C', 0, 0), ('M+', 0, 1), ('M-', 0, 2), ('MR', 0, 3), ('MS', 0, 4),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('x^y', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('√', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('+/-', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('Adv', 4, 4)
        ]
        
        for (text, row, col) in basic_buttons:
            if text in '0123456789':
                btn = tk.Button(self.basic_frame, text=text, command=lambda t=text: self.on_digit_click(t))
            elif text == '=':
                btn = tk.Button(self.basic_frame, text=text, command=self.on_equals_click)
            elif text == 'C':
                btn = tk.Button(self.basic_frame, text=text, command=self.on_clear_click)
            elif text == '.':
                btn = tk.Button(self.basic_frame, text=text, command=self.on_decimal_click)
            elif text == '√':
                btn = tk.Button(self.basic_frame, text=text, command=self.on_sqrt_click)
            elif text == 'x^y':
                btn = tk.Button(self.basic_frame, text=text, command=lambda: self.on_operation_click('x^y'))
            elif text == '+/-':
                btn = tk.Button(self.basic_frame, text=text, command=self.on_change_sign_click)
            elif text == 'M+':
                btn = tk.Button(self.basic_frame, text=text, command=lambda: self.on_memory_add(0))
            elif text == 'M-':
                btn = tk.Button(self.basic_frame, text=text, command=lambda: self.on_memory_subtract(0))
            elif text == 'MR':
                btn = tk.Button(self.basic_frame, text=text, command=lambda: self.on_memory_recall(0))
            elif text == 'MS':
                btn = tk.Button(self.basic_frame, text=text, command=lambda: self.on_memory_store(0))
            elif text == 'Adv':
                btn = tk.Button(self.basic_frame, text=text, command=self.toggle_advanced_mode)
            else:  # +, -, *, /
                btn = tk.Button(self.basic_frame, text=text, command=lambda t=text: self.on_operation_click(t))
            
            btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Configure grid weights for basic frame
        for i in range(5):
            self.basic_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.basic_frame.grid_columnconfigure(i, weight=1)
        
        # Advanced buttons
        advanced_buttons = [
            ('sin', 0, 0), ('asin', 0, 1), ('x²', 0, 2), ('x³', 0, 3),
            ('cos', 1, 0), ('acos', 1, 1), ('1/x', 1, 2), ('Mod', 1, 3),
            ('π', 2, 0), ('e', 2, 1), ('Log', 2, 2), ('Exp', 2, 3),
            ('Dms', 3, 0), ('F-E', 3, 1), ('Int', 3, 2), ('tanh', 3, 3)
        ]
        
        for (text, row, col) in advanced_buttons:
            if text == 'x²':
                btn = tk.Button(self.advanced_frame, text=text, command=self.on_power_click)
            elif text == 'x³':
                btn = tk.Button(self.advanced_frame, text=text, command=self.on_cube_click)
            elif text == '1/x':
                btn = tk.Button(self.advanced_frame, text=text, command=self.on_inverse_click)
            elif text == 'sin':
                btn = tk.Button(self.advanced_frame, text=text, command=self.on_sin_click)
            elif text == 'asin':
                btn = tk.Button(self.advanced_frame, text=text, command=self.on_asin_click)
            elif text == 'cos':
                btn = tk.Button(self.advanced_frame, text=text, command=self.on_cos_click)
            elif text == 'acos':
                btn = tk.Button(self.advanced_frame, text=text, command=self.on_acos_click)
            elif text == 'π':
                btn = tk.Button(self.advanced_frame, text=text, command=lambda: self.on_constant_click(math.pi))
            elif text == 'e':
                btn = tk.Button(self.advanced_frame, text=text, command=lambda: self.on_constant_click(math.e))
            else:
                btn = tk.Button(self.advanced_frame, text=text, command=lambda: self.show_not_implemented())
            
            btn.grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
        
        # Configure grid weights for advanced frame
        for i in range(4):
            self.advanced_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.advanced_frame.grid_columnconfigure(i, weight=1)
        
        # Additional memory buttons if needed
        if len(self.logic.memory) > 1:
            self.memory_frame = tk.Frame(self.root)
            self.memory_frame.pack()
            
            for i in range(len(self.logic.memory)):
                tk.Button(self.memory_frame, text=f"M{i}+", command=lambda x=i: self.on_memory_add(x)).grid(row=0, column=i*5, padx=2)
                tk.Button(self.memory_frame, text=f"M{i}-", command=lambda x=i: self.on_memory_subtract(x)).grid(row=0, column=i*5+1, padx=2)
                tk.Button(self.memory_frame, text=f"MS{i}", command=lambda x=i: self.on_memory_store(x)).grid(row=0, column=i*5+2, padx=2)
                tk.Button(self.memory_frame, text=f"MR{i}", command=lambda x=i: self.on_memory_recall(x)).grid(row=0, column=i*5+3, padx=2)
                tk.Button(self.memory_frame, text=f"MC{i}", command=lambda x=i: self.on_memory_clear(x)).grid(row=0, column=i*5+4, padx=2)
    
    def update_display(self):
        self.current_display.delete(0, tk.END)
        self.current_display.insert(0, self.logic.current_input)
        
        self.history_display.config(state='normal')
        self.history_display.delete(1.0, tk.END)
        for item in self.logic.history[-self.display_lines:]:
            self.history_display.insert(tk.END, item + '\n')
        self.history_display.config(state='disabled')
        self.history_display.yview(tk.END)
    
    def on_digit_click(self, digit):
        self.logic.add_digit(digit)
        self.update_display()
    
    def on_decimal_click(self):
        self.logic.add_decimal_point()
        self.update_display()
    
    def on_clear_click(self):
        self.logic.clear()
        self.update_display()
    
    def on_operation_click(self, op):
        self.logic.set_operation(op)
        self.update_display()
    
    def on_equals_click(self):
        self.logic.calculate()
        self.update_display()
    
    def on_sqrt_click(self):
        self.logic.sqrt()
        self.update_display()
    
    def on_power_click(self):
        self.logic.power()
        self.update_display()
    
    def on_cube_click(self):
        self.logic.cube()
        self.update_display()
    
    def on_sin_click(self):
        self.logic.sin()
        self.update_display()
    
    def on_asin_click(self):
        self.logic.asin()
        self.update_display()
    
    def on_cos_click(self):
        # Would need to implement cos function in logic
        self.show_not_implemented()
    
    def on_acos_click(self):
        self.logic.acos()
        self.update_display()
    
    def on_inverse_click(self):
        self.logic.inverse()
        self.update_display()
    
    def on_change_sign_click(self):
        self.logic.change_sign()
        self.update_display()
    
    def on_constant_click(self, constant):
        self.logic.current_input = str(constant)
        self.update_display()
    
    def on_memory_add(self, cell):
        self.logic.memory_add(cell)
        self.update_display()
    
    def on_memory_subtract(self, cell):
        self.logic.memory_subtract(cell)
        self.update_display()
    
    def on_memory_store(self, cell):
        self.logic.memory_store(cell)
        self.update_display()
    
    def on_memory_recall(self, cell):
        self.logic.memory_recall(cell)
        self.update_display()
    
    def on_memory_clear(self, cell):
        self.logic.memory_clear(cell)
        self.update_display()
    
    def toggle_advanced_mode(self):
        if self.advanced_mode:
            self.advanced_frame.pack_forget()
            self.basic_frame.pack()
        else:
            self.basic_frame.pack_forget()
            self.advanced_frame.pack()
        self.advanced_mode = not self.advanced_mode
    
    def show_not_implemented(self):
        self.logic.current_input = "Not implemented"
        self.update_display()


if __name__ == "__main__":
    student_id = 80121986  # Example ID from the task
    root = tk.Tk()
    app = CalculatorApp(root, student_id)
    root.mainloop()