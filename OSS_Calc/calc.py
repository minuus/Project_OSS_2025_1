import tkinter as tk
import json
import os


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("계산기")
        self.root.geometry("500x600")

        self.expression = ""
        self.history = []
        self.history_file = "calc_history.json"
        self.load_history()

        # 메인 프레임
        main_frame = tk.Frame(root)
        main_frame.pack(expand=True, fill="both")

        # 왼쪽 프레임 (계산기)
        calc_frame = tk.Frame(main_frame)
        calc_frame.pack(side="left", expand=True, fill="both")

        # 오른쪽 프레임 (히스토리)
        history_frame = tk.Frame(main_frame, bg='#f0f0f0', width=200)
        history_frame.pack(side="right", fill="both", padx=5, pady=5)
        history_frame.pack_propagate(False)  # 프레임 크기 고정

        # 히스토리 레이블
        tk.Label(history_frame, text="계산 기록", font=("Arial", 12, "bold"), bg='#f0f0f0').pack(pady=5)

        # 히스토리 리스트박스
        self.history_listbox = tk.Listbox(history_frame, font=("Arial", 10), height=15)
        self.history_listbox.pack(fill="both", padx=5, pady=5, expand=True)
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)

        # 히스토리 삭제 버튼
        clear_btn = tk.Button(history_frame, text="기록 삭제", command=self.clear_history)
        clear_btn.pack(pady=5)

        # 입력창
        self.entry = tk.Entry(calc_frame, font=("Arial", 24), justify="right")
        self.entry.pack(fill="both", ipadx=8, ipady=15, padx=10, pady=10)

        # 버튼 생성
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', 'C', '+'],
            ['=']
        ]

        for row in buttons:
            frame = tk.Frame(calc_frame)
            frame.pack(expand=True, fill="both")
            for char in row:
                btn = tk.Button(
                    frame,
                    text=char,
                    font=("Arial", 18),
                    command=lambda ch=char: self.on_click(ch)
                )
                btn.pack(side="left", expand=True, fill="both")

        # 히스토리 표시 업데이트
        self.update_history_display()

    def load_history(self):
        """저장된 히스토리를 불러옵니다."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                    # 최대 10개까지만 유지
                    self.history = self.history[-10:]
        except Exception:
            self.history = []

    def save_history(self):
        """히스토리를 파일에 저장합니다."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False)
        except Exception:
            pass

    def update_history_display(self):
        """히스토리 표시를 업데이트합니다."""
        self.history_listbox.delete(0, tk.END)
        for item in reversed(self.history):  # 최신 항목이 위에 오도록
            self.history_listbox.insert(0, f"{item['expression']} = {item['result']}")

    def add_to_history(self, expression, result):
        """히스토리에 새 항목을 추가합니다."""
        self.history.append({
            'expression': expression,
            'result': result
        })
        if len(self.history) > 10:  # 최대 10개까지만 유지
            self.history.pop(0)
        self.save_history()
        self.update_history_display()

    def clear_history(self):
        """히스토리를 모두 삭제합니다."""
        self.history = []
        self.save_history()
        self.update_history_display()

    def on_history_select(self, event):
        """히스토리 항목 선택 시 호출됩니다."""
        if not self.history_listbox.curselection():
            return
        
        selected = self.history_listbox.get(self.history_listbox.curselection())
        expression = selected.split(' = ')[0]  # 수식 부분만 추출
        
        self.expression = expression
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                result = str(eval(self.expression))
                self.add_to_history(self.expression, result)  # 히스토리에 추가
                self.expression = result
            except Exception:
                self.expression = "에러"
        else:
            self.expression += str(char)

        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)



