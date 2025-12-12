import customtkinter as ctk
import requests
import threading
from datetime import datetime

# Theme Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class UnitConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW SETUP ---
        self.title("Modern Converter")
        self.geometry("900x700") # Standard starting size
        self.resizable(True, True)
        
        # Track full screen state
        self.is_fullscreen = False

        # Bind Keys
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)

        # API setup
        self.api_key = "YOUR_API_KEY_HERE"  
        self.exchange_rates = {}

        # --- UI LAYOUT ---
        
        # 1. Top Bar Frame (Holds the Toggle Switch)
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=20, pady=10)

        # Full Screen Switch
        self.fs_switch = ctk.CTkSwitch(self.top_bar, text="Full Screen", command=self.toggle_fullscreen_switch)
        self.fs_switch.pack(side="right")

        # 2. Main Container (Centers the content)
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both")

        # 3. Header
        self.header_label = ctk.CTkLabel(self.container, text="Utility Hub", font=("Roboto Medium", 32))
        self.header_label.pack(pady=(10, 20))

        # 4. Tabs
        self.tabview = ctk.CTkTabview(self.container, width=700, height=550)
        self.tabview.pack(pady=10, expand=True)

        self.tabview.add("Length")
        self.tabview.add("Temperature")
        self.tabview.add("BMI")
        self.tabview.add("Currency")

        # Setup Converters
        self.setup_length_tab()
        self.setup_temp_tab()
        self.setup_bmi_tab()
        self.setup_currency_tab()

        # Background tasks
        threading.Thread(target=self.load_currency_rates, daemon=True).start()

    # --- FULL SCREEN LOGIC ---
    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        
        # Sync the switch with the state
        if self.is_fullscreen:
            self.fs_switch.select()
        else:
            self.fs_switch.deselect()

    def toggle_fullscreen_switch(self):
        # Triggered by the UI switch
        self.is_fullscreen = self.fs_switch.get()
        self.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.attributes("-fullscreen", False)
            self.fs_switch.deselect()

    # --- UI SETUP FUNCTIONS (Standard) ---

    def setup_length_tab(self):
        tab = self.tabview.tab("Length")
        self.length_units = {
            "Meters": 1, "Kilometers": 1000, "Centimeters": 0.01,
            "Millimeters": 0.001, "Miles": 1609.34, "Yards": 0.9144,
            "Feet": 0.3048, "Inches": 0.0254
        }
        
        # Use grid layout for better centering
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Convert Length", font=("Roboto", 20)).pack(pady=20)

        self.length_entry = ctk.CTkEntry(tab, placeholder_text="Enter value", width=250, height=40, font=("Arial", 14))
        self.length_entry.pack(pady=10)
        self.length_entry.insert(0, "1")

        self.len_from_menu = ctk.CTkOptionMenu(tab, values=list(self.length_units.keys()), width=200, command=self.convert_length)
        self.len_from_menu.pack(pady=10)
        self.len_from_menu.set("Meters")

        ctk.CTkLabel(tab, text="⬇", font=("Arial", 24)).pack(pady=5)

        self.len_to_menu = ctk.CTkOptionMenu(tab, values=list(self.length_units.keys()), width=200, command=self.convert_length)
        self.len_to_menu.pack(pady=10)
        self.len_to_menu.set("Kilometers")

        self.length_result = ctk.CTkButton(tab, text="0.001 Kilometers", width=300, height=50, font=("Arial", 18, "bold"),
                                          fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.length_result.pack(pady=20)
        self.length_entry.bind("<KeyRelease>", lambda e: self.convert_length())

    def setup_temp_tab(self):
        tab = self.tabview.tab("Temperature")
        self.temp_units = ["Celsius", "Fahrenheit", "Kelvin"]

        ctk.CTkLabel(tab, text="Convert Temperature", font=("Roboto", 20)).pack(pady=20)

        self.temp_entry = ctk.CTkEntry(tab, placeholder_text="Value", width=250, height=40, font=("Arial", 14))
        self.temp_entry.pack(pady=10)
        self.temp_entry.insert(0, "0")

        self.temp_from_menu = ctk.CTkOptionMenu(tab, values=self.temp_units, width=200, command=self.convert_temp)
        self.temp_from_menu.pack(pady=10)
        
        ctk.CTkLabel(tab, text="⬇", font=("Arial", 24)).pack(pady=5)

        self.temp_to_menu = ctk.CTkOptionMenu(tab, values=self.temp_units, width=200, command=self.convert_temp)
        self.temp_to_menu.pack(pady=10)
        self.temp_to_menu.set("Fahrenheit")

        self.temp_result = ctk.CTkButton(tab, text="32.00 Fahrenheit", width=300, height=50, font=("Arial", 18, "bold"),
                                        fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.temp_result.pack(pady=20)
        self.temp_entry.bind("<KeyRelease>", lambda e: self.convert_temp())

    def setup_bmi_tab(self):
        tab = self.tabview.tab("BMI")
        ctk.CTkLabel(tab, text="Body Mass Index", font=("Roboto", 20)).pack(pady=15)

        self.height_entry = ctk.CTkEntry(tab, placeholder_text="Height (m)", width=250, height=40)
        self.height_entry.pack(pady=5)
        self.height_entry.insert(0, "1.75")
        ctk.CTkLabel(tab, text="meters", font=("Arial", 10)).pack()

        self.weight_entry = ctk.CTkEntry(tab, placeholder_text="Weight (kg)", width=250, height=40)
        self.weight_entry.pack(pady=5)
        self.weight_entry.insert(0, "70")
        ctk.CTkLabel(tab, text="kg", font=("Arial", 10)).pack()

        btn = ctk.CTkButton(tab, text="Calculate BMI", width=200, command=self.calculate_bmi)
        btn.pack(pady=15)

        self.bmi_result_label = ctk.CTkLabel(tab, text="BMI: 22.9", font=("Roboto", 28, "bold"))
        self.bmi_result_label.pack(pady=5)

        self.bmi_category_label = ctk.CTkLabel(tab, text="Normal Weight", font=("Roboto", 16))
        self.bmi_category_label.pack(pady=5)

        self.bmi_progress = ctk.CTkProgressBar(tab, width=300)
        self.bmi_progress.pack(pady=15)
        self.bmi_progress.set(0.5)

        self.height_entry.bind("<KeyRelease>", lambda e: self.calculate_bmi())
        self.weight_entry.bind("<KeyRelease>", lambda e: self.calculate_bmi())

    def setup_currency_tab(self):
        tab = self.tabview.tab("Currency")
        self.currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "INR", "BRL"]

        ctk.CTkLabel(tab, text="Global Currency", font=("Roboto", 20)).pack(pady=20)

        self.curr_entry = ctk.CTkEntry(tab, placeholder_text="Amount", width=250, height=40, font=("Arial", 14))
        self.curr_entry.pack(pady=10)
        self.curr_entry.insert(0, "1")

        self.curr_from_menu = ctk.CTkOptionMenu(tab, values=self.currencies, width=200, command=self.convert_currency)
        self.curr_from_menu.pack(pady=10)

        ctk.CTkLabel(tab, text="⬇", font=("Arial", 24)).pack(pady=5)

        self.curr_to_menu = ctk.CTkOptionMenu(tab, values=self.currencies, width=200, command=self.convert_currency)
        self.curr_to_menu.pack(pady=10)
        self.curr_to_menu.set("EUR")

        self.curr_result = ctk.CTkButton(tab, text="Loading...", width=300, height=50, font=("Arial", 18, "bold"),
                                        fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.curr_result.pack(pady=20)
        
        self.curr_status = ctk.CTkLabel(tab, text="Fetching rates...", font=("Arial", 10))
        self.curr_status.pack(side="bottom", pady=10)
        self.curr_entry.bind("<KeyRelease>", lambda e: self.convert_currency())

    # --- CALCULATION LOGIC ---
    def convert_length(self, _=None):
        try:
            val = float(self.length_entry.get())
            u_from = self.length_units[self.len_from_menu.get()]
            u_to = self.length_units[self.len_to_menu.get()]
            result = (val * u_from) / u_to
            self.length_result.configure(text=f"{result:.4f} {self.len_to_menu.get()}")
        except ValueError:
            self.length_result.configure(text="Invalid Input")

    def convert_temp(self, _=None):
        try:
            val = float(self.temp_entry.get())
            from_u = self.temp_from_menu.get()
            to_u = self.temp_to_menu.get()
            if from_u == "Fahrenheit": c = (val - 32) * 5/9
            elif from_u == "Kelvin": c = val - 273.15
            else: c = val
            if to_u == "Fahrenheit": res = (c * 9/5) + 32
            elif to_u == "Kelvin": res = c + 273.15
            else: res = c
            self.temp_result.configure(text=f"{res:.2f} {to_u}")
        except ValueError:
            self.temp_result.configure(text="Invalid Input")

    def calculate_bmi(self, _=None):
        try:
            h = float(self.height_entry.get())
            w = float(self.weight_entry.get())
            if h <= 0 or w <= 0: return
            bmi = w / (h ** 2)
            self.bmi_result_label.configure(text=f"BMI: {bmi:.1f}")
            normalized_bmi = min(max((bmi - 10) / 30, 0), 1) 
            self.bmi_progress.set(normalized_bmi)
            if bmi < 18.5:
                self.bmi_category_label.configure(text="Underweight", text_color="#3B8ED0")
                self.bmi_progress.configure(progress_color="#3B8ED0")
            elif bmi < 25:
                self.bmi_category_label.configure(text="Normal Weight", text_color="#2CC985")
                self.bmi_progress.configure(progress_color="#2CC985")
            elif bmi < 30:
                self.bmi_category_label.configure(text="Overweight", text_color="#E1A337")
                self.bmi_progress.configure(progress_color="#E1A337")
            else:
                self.bmi_category_label.configure(text="Obesity", text_color="#C42B1C")
                self.bmi_progress.configure(progress_color="#C42B1C")
        except ValueError:
            pass

    def load_currency_rates(self):
        try:
            if self.api_key == "YOUR_API_KEY_HERE": raise Exception("No API Key")
            url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/USD"
            response = requests.get(url, timeout=5)
            data = response.json()
            if data["result"] == "success":
                self.exchange_rates = data["conversion_rates"]
                self.curr_status.configure(text=f"Updated: {datetime.now().strftime('%H:%M')}")
        except:
            self.exchange_rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "INR": 83.10, "JPY": 147.5, "CAD": 1.36, "AUD": 1.52, "CHF": 0.88, "CNY": 7.25, "BRL": 4.95}
            self.curr_status.configure(text="Using Offline Rates")
        self.convert_currency()

    def convert_currency(self, _=None):
        try:
            val = float(self.curr_entry.get())
            from_c = self.curr_from_menu.get()
            to_c = self.curr_to_menu.get()
            if not self.exchange_rates:
                self.curr_result.configure(text="Loading...")
                return
            usd_val = val if from_c == "USD" else val / self.exchange_rates.get(from_c, 1)
            res = usd_val if to_c == "USD" else usd_val * self.exchange_rates.get(to_c, 1)
            self.curr_result.configure(text=f"{res:.2f} {to_c}")
        except ValueError:
            self.curr_result.configure(text="Invalid Input")

if __name__ == "__main__":
    app = UnitConverterApp()
    app.mainloop()
