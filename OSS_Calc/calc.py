import tkinter as tk
from tkinter import ttk


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("계산기")
        self.root.geometry("300x500")

        self.expression = ""
        self.memory = 0  # 메모리 저장 변수

        # 입력창
        self.entry = tk.Entry(root, font=("Arial", 24), justify="right")
        self.entry.pack(fill="both", ipadx=8, ipady=15, padx=10, pady=10)

        # 메모리 상태 표시
        self.memory_label = tk.Label(root, text="M: 0", font=("Arial", 12), anchor="e")
        self.memory_label.pack(fill="x", padx=10)

        # 메모리 버튼 프레임
        memory_frame = tk.Frame(root)
        memory_frame.pack(expand=True, fill="both")
        
        memory_buttons = ['MC', 'MR', 'M+', 'M-', 'MS']
        for btn_text in memory_buttons:
            btn = tk.Button(
                memory_frame,
                text=btn_text,
                font=("Arial", 12),
                command=lambda x=btn_text: self.memory_operation(x)
            )
            btn.pack(side="left", expand=True, fill="both")

        # 숫자 및 연산 버튼
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', 'C', '+'],
            ['=']
        ]

        for row in buttons:
            frame = tk.Frame(root)
            frame.pack(expand=True, fill="both")
            for char in row:
                btn = tk.Button(
                    frame,
                    text=char,
                    font=("Arial", 18),
                    command=lambda ch=char: self.on_click(ch)
                )
                btn.pack(side="left", expand=True, fill="both")

    def memory_operation(self, operation):
        try:
            current_value = float(self.entry.get()) if self.entry.get() else 0
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "에러")
            return

        if operation == "MC":  # Memory Clear
            self.memory = 0
        elif operation == "MR":  # Memory Recall
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(self.memory))
            self.expression = str(self.memory)
        elif operation == "M+":  # Memory Add
            self.memory += current_value
        elif operation == "M-":  # Memory Subtract
            self.memory -= current_value
        elif operation == "MS":  # Memory Store
            self.memory = current_value

        # 메모리 상태 업데이트
        self.memory_label.config(text=f"M: {self.memory}")

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                self.expression = str(eval(self.expression))
            except Exception:
                self.expression = "에러"
        else:
            self.expression += str(char)

        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)



