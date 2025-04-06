import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

USD_TO_SAR = 3.75

class PriceCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("حاسبة تسعير الطباعة ثلاثية الأبعاد")
        self.geometry("700x550")
        self.minsize(700, 550)

        self.dark_mode = tk.BooleanVar(value=False)

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self, text="بيانات الطباعة")
        input_frame.pack(fill="x", padx=10, pady=10)

        self.entries = {}

        fields = [("مدة الطباعة (ساعات):", "time"),
                  ("وزن الفتيل (جرام):", "weight"),
                  ("سعر الفتيل ($ لكل جرام):", "filament_price")]

        for i, (label, key) in enumerate(fields):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(input_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[key] = entry

        input_frame.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="احسب السعر", command=self.calculate).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(btn_frame, text="إعادة تعيين", command=self.reset_fields).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Checkbutton(btn_frame, text="الوضع الداكن", variable=self.dark_mode, command=self.apply_theme).pack(side="left", expand=True, fill="x", padx=5)

        result_frame = ttk.LabelFrame(self, text="نتيجة الحساب")
        result_frame.pack(fill="both", padx=10, pady=10, expand=True)

        self.result_text = scrolledtext.ScrolledText(result_frame, state="disabled", wrap="word")
        self.result_text.pack(expand=True, fill="both", padx=5, pady=5)

    def calculate(self):
        try:
            time = float(self.entries['time'].get())
            weight = float(self.entries['weight'].get())
            filament_price_usd_per_g = float(self.entries['filament_price'].get())

            material_cost_usd = filament_price_usd_per_g * weight
            material_cost_sar = material_cost_usd * USD_TO_SAR
            machine_cost_sar = time * 7.5

            total_cost_sar = material_cost_sar + machine_cost_sar

            prices = {
                'تكلفة المواد': (material_cost_sar, material_cost_usd),
                'تكلفة الطابعة': (machine_cost_sar, machine_cost_sar / USD_TO_SAR),
                'التكلفة الإجمالية': (total_cost_sar, total_cost_sar / USD_TO_SAR),
                'السعر المقترح (30٪ ربح)': (total_cost_sar * 1.3, (total_cost_sar * 1.3) / USD_TO_SAR),
                'السعر المقترح (50٪ ربح)': (total_cost_sar * 1.5, (total_cost_sar * 1.5) / USD_TO_SAR),
                'السعر المقترح (100٪ ربح)': (total_cost_sar * 2.0, (total_cost_sar * 2.0) / USD_TO_SAR),
            }

            self.show_results(prices)

        except ValueError:
            messagebox.showerror("خطأ", "تأكد من إدخال أرقام صحيحة في كل الحقول.")

    def show_results(self, prices):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        for label, (sar, usd) in prices.items():
            self.result_text.insert(tk.END, f"{label}: {sar:.2f} ريال سعودي ({usd:.2f} دولار أمريكي)\n")

        self.result_text.config(state="disabled")

    def reset_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")

    def apply_theme(self):
        style = ttk.Style()

        if self.dark_mode.get():
            self.configure(bg="#2b2b2b")
            style.theme_use("clam")
            style.configure('.', background="#2b2b2b", foreground="#ffffff", fieldbackground="#3b3b3b")
            style.map("TButton", background=[("active", "#4a4a4a")])
            self.result_text.configure(bg="#3b3b3b", fg="#ffffff")
        else:
            self.configure(bg="#f0f0f0")
            style.theme_use("default")
            style.configure('.', background="#f0f0f0", foreground="#000000", fieldbackground="#ffffff")
            style.map("TButton", background=[("active", "#e5e5e5")])
            self.result_text.configure(bg="#ffffff", fg="#000000")

if __name__ == "__main__":
    app = PriceCalculator()
    app.mainloop()
