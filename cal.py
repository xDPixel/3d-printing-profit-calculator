import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

USD_TO_SAR = 3.75

translations = {
    'en': {
        'title': '3D Printing Pricing Calculator',
        'input_data': 'Printing Data',
        'time': 'Printing Duration (hours):',
        'weight': 'Filament Weight (g):',
        'filament_price': 'Filament Price ($ per gram):',
        'calculate': 'Calculate Price',
        'reset': 'Reset',
        'dark_mode': 'Dark Mode',
        'result': 'Calculation Result',
        'error': 'Error',
        'error_msg': 'Please ensure all fields contain valid numbers.',
        'material_cost': 'Material Cost',
        'printer_cost': 'Printer Cost',
        'total_cost': 'Total Cost',
        'suggested_price': 'Suggested Price',
        'profit_30': ' (30% Profit)',
        'profit_50': ' (50% Profit)',
        'profit_100': ' (100% Profit)',
        'currency_sar': 'SAR',
        'currency_usd': 'USD'
    },
    'ar': {
        'title': 'حاسبة تسعير الطباعة ثلاثية الأبعاد',
        'input_data': 'بيانات الطباعة',
        'time': 'مدة الطباعة (ساعات):',
        'weight': 'وزن الفتيل (جرام):',
        'filament_price': 'سعر الفتيل ($ لكل جرام):',
        'calculate': 'احسب السعر',
        'reset': 'إعادة تعيين',
        'dark_mode': 'الوضع الداكن',
        'result': 'نتيجة الحساب',
        'error': 'خطأ',
        'error_msg': 'تأكد من إدخال أرقام صحيحة في كل الحقول.',
        'material_cost': 'تكلفة المواد',
        'printer_cost': 'تكلفة الطابعة',
        'total_cost': 'التكلفة الإجمالية',
        'suggested_price': 'السعر المقترح',
        'profit_30': ' (30٪ ربح)',
        'profit_50': ' (50٪ ربح)',
        'profit_100': ' (100٪ ربح)',
        'currency_sar': 'ريال سعودي',
        'currency_usd': 'دولار أمريكي'
    }
}

class PriceCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.language = 'ar'
        self.dark_mode = tk.BooleanVar(value=False)

        self.title(translations[self.language]['title'])
        self.geometry("700x550")
        self.minsize(700, 550)

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.input_frame = ttk.LabelFrame(self, text=translations[self.language]['input_data'])
        self.input_frame.pack(fill="x", padx=10, pady=10)

        self.entries = {}

        self.fields = [('time', translations[self.language]['time']),
                       ('weight', translations[self.language]['weight']),
                       ('filament_price', translations[self.language]['filament_price'])]

        for i, (key, label) in enumerate(self.fields):
            ttk.Label(self.input_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self.input_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[key] = entry

        self.input_frame.columnconfigure(1, weight=1)

        self.btn_frame = ttk.Frame(self)
        self.btn_frame.pack(fill="x", padx=10, pady=5)

        self.calc_btn = ttk.Button(self.btn_frame, text=translations[self.language]['calculate'], command=self.calculate)
        self.calc_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.reset_btn = ttk.Button(self.btn_frame, text=translations[self.language]['reset'], command=self.reset_fields)
        self.reset_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.theme_check = ttk.Checkbutton(self.btn_frame, text=translations[self.language]['dark_mode'], variable=self.dark_mode, command=self.apply_theme)
        self.theme_check.pack(side="left", expand=True, fill="x", padx=5)

        self.lang_btn = ttk.Button(self.btn_frame, text="EN/AR", command=self.switch_language)
        self.lang_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.result_frame = ttk.LabelFrame(self, text=translations[self.language]['result'])
        self.result_frame.pack(fill="both", padx=10, pady=10, expand=True)

        self.result_text = scrolledtext.ScrolledText(self.result_frame, state="disabled", wrap="word")
        self.result_text.pack(expand=True, fill="both", padx=5, pady=5)

    def switch_language(self):
        self.language = 'en' if self.language == 'ar' else 'ar'
        self.update_ui()

    def update_ui(self):
        trans = translations[self.language]
        self.title(trans['title'])
        self.input_frame.config(text=trans['input_data'])
        for i, (key, _) in enumerate(self.fields):
            self.input_frame.grid_slaves(row=i, column=0)[0].config(text=trans[key])
        self.calc_btn.config(text=trans['calculate'])
        self.reset_btn.config(text=trans['reset'])
        self.theme_check.config(text=trans['dark_mode'])
        self.result_frame.config(text=trans['result'])

    def calculate(self):
        try:
            time = float(self.entries['time'].get())
            weight = float(self.entries['weight'].get())
            filament_price_usd_per_g = float(self.entries['filament_price'].get())

            material_cost_usd = filament_price_usd_per_g * weight
            material_cost_sar = material_cost_usd * USD_TO_SAR
            machine_cost_sar = time * 7.5

            total_cost_sar = material_cost_sar + machine_cost_sar

            self.show_results(material_cost_sar, machine_cost_sar, total_cost_sar)

        except ValueError:
            messagebox.showerror(translations[self.language]['error'], translations[self.language]['error_msg'])

    def show_results(self, material_sar, machine_sar, total_sar):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        trans = translations[self.language]
        results = [
            (trans['material_cost'], material_sar),
            (trans['printer_cost'], machine_sar),
            (trans['total_cost'], total_sar),
            (trans['suggested_price'] + trans['profit_30'], total_sar * 1.3),
            (trans['suggested_price'] + trans['profit_50'], total_sar * 1.5),
            (trans['suggested_price'] + trans['profit_100'], total_sar * 2.0)
        ]

        for label, sar in results:
            usd = sar / USD_TO_SAR
            self.result_text.insert(tk.END, f"{label}: {sar:.2f} {trans['currency_sar']} ({usd:.2f} {trans['currency_usd']})\n")

        self.result_text.config(state="disabled")

    def reset_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")

    def apply_theme(self):
        style = ttk.Style()
        theme = "clam" if self.dark_mode.get() else "default"
        style.theme_use(theme)

if __name__ == "__main__":
    app = PriceCalculator()
    app.mainloop()
