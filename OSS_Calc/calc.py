import tkinter as tk
from tkinter import ttk


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("계산기")
        self.root.geometry("400x600")

        self.expression = ""
        self.conversion_mode = False
        
        # 탭 생성
        self.tab_control = ttk.Notebook(root)
        
        # 기본 계산기 탭
        self.calc_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.calc_tab, text='기본 계산기')
        
        # 단위 변환 탭
        self.conv_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.conv_tab, text='단위 변환')
        
        self.tab_control.pack(expand=True, fill="both")

        # 기본 계산기 UI
        self.setup_calculator()
        
        # 단위 변환 UI
        self.setup_converter()

    def setup_calculator(self):
        # 입력창
        self.entry = tk.Entry(self.calc_tab, font=("Arial", 24), justify="right")
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
            frame = tk.Frame(self.calc_tab)
            frame.pack(expand=True, fill="both")
            for char in row:
                btn = tk.Button(
                    frame,
                    text=char,
                    font=("Arial", 18),
                    command=lambda ch=char: self.on_click(ch)
                )
                btn.pack(side="left", expand=True, fill="both")

    def setup_converter(self):
        # 변환 유형 선택
        self.conv_types = {
            "길이": {
                "미터(m)": 1,
                "킬로미터(km)": 1000,
                "센티미터(cm)": 0.01,
                "밀리미터(mm)": 0.001,
                "인치(inch)": 0.0254,
                "피트(ft)": 0.3048
            },
            "무게": {
                "그램(g)": 1,
                "킬로그램(kg)": 1000,
                "밀리그램(mg)": 0.001,
                "파운드(lb)": 453.592,
                "온스(oz)": 28.3495
            },
            "온도": {
                "섭씨(°C)": "C",
                "화씨(°F)": "F",
                "켈빈(K)": "K"
            }
        }

        # 변환 유형 선택 콤보박스
        tk.Label(self.conv_tab, text="변환 유형:", font=("Arial", 12)).pack(pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(self.conv_tab, textvariable=self.type_var, values=list(self.conv_types.keys()))
        self.type_combo.pack(pady=5)
        self.type_combo.bind('<<ComboboxSelected>>', self.update_units)

        # 입력 프레임
        input_frame = ttk.Frame(self.conv_tab)
        input_frame.pack(pady=10, fill="x", padx=10)

        # 입력값
        tk.Label(input_frame, text="입력값:", font=("Arial", 12)).pack(side="left")
        self.conv_input = tk.Entry(input_frame, font=("Arial", 12))
        self.conv_input.pack(side="left", padx=5, expand=True, fill="x")

        # 단위 선택
        unit_frame = ttk.Frame(self.conv_tab)
        unit_frame.pack(pady=10, fill="x", padx=10)

        # 시작 단위
        tk.Label(unit_frame, text="시작 단위:", font=("Arial", 12)).pack(side="left")
        self.from_unit_var = tk.StringVar()
        self.from_unit_combo = ttk.Combobox(unit_frame, textvariable=self.from_unit_var)
        self.from_unit_combo.pack(side="left", padx=5)

        # 목표 단위
        tk.Label(unit_frame, text="목표 단위:", font=("Arial", 12)).pack(side="left")
        self.to_unit_var = tk.StringVar()
        self.to_unit_combo = ttk.Combobox(unit_frame, textvariable=self.to_unit_var)
        self.to_unit_combo.pack(side="left", padx=5)

        # 변환 버튼
        tk.Button(self.conv_tab, text="변환", font=("Arial", 12), command=self.convert).pack(pady=10)

        # 결과 표시
        self.result_var = tk.StringVar()
        tk.Label(self.conv_tab, textvariable=self.result_var, font=("Arial", 14)).pack(pady=10)

    def update_units(self, event=None):
        conv_type = self.type_var.get()
        if conv_type in self.conv_types:
            units = list(self.conv_types[conv_type].keys())
            self.from_unit_combo['values'] = units
            self.to_unit_combo['values'] = units
            self.from_unit_combo.set(units[0])
            self.to_unit_combo.set(units[1])

    def convert(self):
        try:
            value = float(self.conv_input.get())
            conv_type = self.type_var.get()
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()

            if conv_type == "온도":
                result = self.convert_temperature(value, from_unit, to_unit)
            else:
                # 기준 단위로 변환
                base_value = value * self.conv_types[conv_type][from_unit]
                # 목표 단위로 변환
                result = base_value / self.conv_types[conv_type][to_unit]

            self.result_var.set(f"결과: {result:.4f}")
        except ValueError:
            self.result_var.set("올바른 숫자를 입력하세요")
        except Exception as e:
            self.result_var.set(f"오류: {str(e)}")

    def convert_temperature(self, value, from_unit, to_unit):
        # 섭씨로 변환
        if from_unit == "화씨(°F)":
            celsius = (value - 32) * 5/9
        elif from_unit == "켈빈(K)":
            celsius = value - 273.15
        else:  # 섭씨
            celsius = value

        # 목표 단위로 변환
        if to_unit == "화씨(°F)":
            return celsius * 9/5 + 32
        elif to_unit == "켈빈(K)":
            return celsius + 273.15
        else:  # 섭씨
            return celsius

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



