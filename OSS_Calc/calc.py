import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("모던 계산기")
        self.root.geometry("320x580")
        self.root.configure(bg='#2C3E50')  # 진한 남색 배경

        # 스타일 설정
        self.style = ttk.Style()
        self.style.configure('Memory.TButton', font=('Arial', 11), padding=5)
        
        self.expression = ""
        self.memory = 0

        # 프레임 생성
        main_frame = tk.Frame(root, bg='#2C3E50', padx=10, pady=10)
        main_frame.pack(expand=True, fill="both")

        # 입력창
        entry_frame = tk.Frame(main_frame, bg='#2C3E50', pady=10)
        entry_frame.pack(fill="x")
        
        self.entry = tk.Entry(
            entry_frame,
            font=("Arial", 28),
            justify="right",
            bd=0,
            bg='#34495E',
            fg='white',
            insertbackground='white'
        )
        self.entry.pack(fill="both", ipady=15)

        # 메모리 상태 표시
        self.memory_label = tk.Label(
            main_frame,
            text="M: 0",
            font=("Arial", 12),
            anchor="e",
            bg='#2C3E50',
            fg='#3498DB'
        )
        self.memory_label.pack(fill="x", pady=(0, 10))

        # 메모리 버튼 프레임
        memory_frame = tk.Frame(main_frame, bg='#2C3E50')
        memory_frame.pack(fill="x", pady=(0, 10))
        
        # 메모리 버튼을 담을 그리드 생성
        memory_frame.grid_columnconfigure(0, weight=1)
        memory_frame.grid_columnconfigure(1, weight=1)
        memory_frame.grid_columnconfigure(2, weight=1)
        memory_frame.grid_columnconfigure(3, weight=1)
        memory_frame.grid_columnconfigure(4, weight=1)
        
        memory_buttons = ['MC', 'MR', 'M+', 'M-', 'MS']
        for i, btn_text in enumerate(memory_buttons):
            btn = tk.Button(
                memory_frame,
                text=btn_text,
                font=("Arial", 11),
                command=lambda x=btn_text: self.memory_operation(x),
                bg='#3498DB',
                fg='white',
                activebackground='#2980B9',
                activeforeground='white',
                bd=0,
                relief='flat',
                padx=5,
                pady=5
            )
            btn.grid(row=0, column=i, sticky="nsew", padx=2)

        # 숫자 및 연산 버튼을 위한 그리드 프레임
        buttons_frame = tk.Frame(main_frame, bg='#2C3E50')
        buttons_frame.pack(expand=True, fill="both")
        
        # 그리드 설정
        for i in range(5):  # 5행
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):  # 4열
            buttons_frame.grid_columnconfigure(i, weight=1)

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', 'C', '+']
        ]

        # 일반 버튼들 배치
        for i, row in enumerate(buttons):
            for j, char in enumerate(row):
                btn = tk.Button(
                    buttons_frame,
                    text=char,
                    font=("Arial", 18),
                    command=lambda ch=char: self.on_click(ch),
                    bg='#34495E' if char in ['/', '*', '-', '+', 'C'] else '#445566',
                    fg='white',
                    activebackground='#2C3E50',
                    activeforeground='white',
                    bd=0,
                    relief='flat',
                    padx=10,
                    pady=10
                )
                btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)

        # = 버튼 (마지막 줄 전체 차지)
        equals_btn = tk.Button(
            buttons_frame,
            text='=',
            font=("Arial", 18),
            command=lambda: self.on_click('='),
            bg='#E74C3C',
            fg='white',
            activebackground='#C0392B',
            activeforeground='white',
            bd=0,
            relief='flat',
            padx=10,
            pady=10
        )
        equals_btn.grid(row=4, column=0, columnspan=4, sticky="nsew", padx=2, pady=2)

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



