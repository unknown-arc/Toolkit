import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math

class DataCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Data Calculator - Everyday Toolkit")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # History storage
        self.history = []
        
        # Configure styles
        self.setup_styles()
        
        # Create main container
        self.create_widgets()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.colors = {
            'primary': '#3B82F6',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'light': '#F3F4F6',
            'dark': '#1F2937'
        }
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title frame
        title_frame = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🧮 Data Calculator - Everyday Toolkit",
            font=("Arial", 24, "bold"),
            fg="white",
            bg=self.colors['primary']
        )
        title_label.pack(pady=30)
        
        # Main container with notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_bill_splitter_tab()
        self.create_discount_tab()
        self.create_percentage_tab()
        self.create_gpa_tab()
        self.create_tax_tab()
        self.create_interest_tab()
        self.create_history_tab()
        
    def create_bill_splitter_tab(self):
        """Create Bill Splitter tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💰 Bill Splitter")
        
        # Input frame
        input_frame = tk.LabelFrame(tab, text="Input Parameters", font=("Arial", 12, "bold"),
                                   bg=self.colors['light'], padx=20, pady=20)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Bill amount
        tk.Label(input_frame, text="Total Bill Amount ($):", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.bill_amount = tk.DoubleVar(value=100.0)
        tk.Entry(input_frame, textvariable=self.bill_amount, font=("Arial", 11),
                width=20).grid(row=0, column=1, pady=5, padx=5)
        
        # Tip percentage
        tk.Label(input_frame, text="Tip Percentage (%):", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.tip_percent = tk.DoubleVar(value=18.0)
        tk.Scale(input_frame, from_=0, to=50, orient="horizontal", variable=self.tip_percent,
                bg=self.colors['light'], length=200).grid(row=1, column=1, pady=5, padx=5)
        
        # Number of people
        tk.Label(input_frame, text="Number of People:", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
        self.num_people = tk.IntVar(value=4)
        tk.Spinbox(input_frame, from_=1, to=50, textvariable=self.num_people,
                  font=("Arial", 11), width=10).grid(row=2, column=1, pady=5, padx=5)
        
        # Tax percentage
        tk.Label(input_frame, text="Sales Tax (%):", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=3, column=0, sticky="w", pady=5)
        self.tax_percent = tk.DoubleVar(value=8.25)
        tk.Entry(input_frame, textvariable=self.tax_percent, font=("Arial", 11),
                width=20).grid(row=3, column=1, pady=5, padx=5)
        
        # Calculate button
        calc_btn = tk.Button(input_frame, text="🧮 Calculate Split", command=self.calculate_bill_split,
                           bg=self.colors['primary'], fg="white", font=("Arial", 11, "bold"),
                           padx=20, pady=10)
        calc_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Results frame
        self.bill_results_frame = tk.LabelFrame(tab, text="Results", font=("Arial", 12, "bold"),
                                               bg=self.colors['light'], padx=20, pady=20)
        self.bill_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def calculate_bill_split(self):
        """Calculate bill split results"""
        try:
            bill = self.bill_amount.get()
            tip_pct = self.tip_percent.get()
            people = self.num_people.get()
            tax_pct = self.tax_percent.get()
            
            if bill <= 0 or people <= 0:
                messagebox.showerror("Error", "Please enter valid positive values")
                return
            
            # Calculate
            tax_amount = bill * (tax_pct / 100)
            tip_amount = bill * (tip_pct / 100)
            total_amount = bill + tax_amount + tip_amount
            per_person = total_amount / people
            
            # Clear previous results
            for widget in self.bill_results_frame.winfo_children():
                widget.destroy()
            
            # Display results in a nice format
            results_text = f"""
            💰 BILL SPLIT RESULTS 💰
            {"="*40}
            
            Bill Amount:      ${bill:.2f}
            Tax ({tax_pct}%):      ${tax_amount:.2f}
            Tip ({tip_pct}%):      ${tip_amount:.2f}
            {"-"*40}
            Total Amount:     ${total_amount:.2f}
            
            👥 Split among {people} people:
            Each Person Pays: ${per_person:.2f}
            {"="*40}
            """
            
            result_label = tk.Label(self.bill_results_frame, text=results_text,
                                   font=("Courier", 11), bg=self.colors['light'],
                                   justify="left")
            result_label.pack(pady=10)
            
            # Add to history
            self.history.append(f"Bill Split: ${bill:.2f}, {tip_pct}% tip, {people} people = ${per_person:.2f}/person")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def create_discount_tab(self):
        """Create Discount Calculator tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🛍️ Discount")
        
        input_frame = tk.LabelFrame(tab, text="Input Parameters", font=("Arial", 12, "bold"),
                                   bg=self.colors['light'], padx=20, pady=20)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Original price
        tk.Label(input_frame, text="Original Price ($):", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.original_price = tk.DoubleVar(value=100.0)
        tk.Entry(input_frame, textvariable=self.original_price, font=("Arial", 11),
                width=20).grid(row=0, column=1, pady=5, padx=5)
        
        # Discount percentage
        tk.Label(input_frame, text="Discount (%):", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.discount_percent = tk.DoubleVar(value=20.0)
        tk.Scale(input_frame, from_=0, to=100, orient="horizontal", variable=self.discount_percent,
                bg=self.colors['light'], length=200).grid(row=1, column=1, pady=5, padx=5)
        
        # Quick buttons
        button_frame = tk.Frame(input_frame, bg=self.colors['light'])
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        discounts = [10, 15, 20, 25, 30, 50]
        for i, disc in enumerate(discounts):
            btn = tk.Button(button_frame, text=f"{disc}%", width=8,
                          command=lambda d=disc: self.set_discount(d),
                          bg=self.colors['primary'], fg="white")
            btn.grid(row=0, column=i, padx=2)
        
        # Calculate button
        calc_btn = tk.Button(input_frame, text="📉 Calculate Discount", command=self.calculate_discount,
                           bg=self.colors['primary'], fg="white", font=("Arial", 11, "bold"),
                           padx=20, pady=10)
        calc_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Results frame
        self.discount_results_frame = tk.LabelFrame(tab, text="Results", font=("Arial", 12, "bold"),
                                                   bg=self.colors['light'], padx=20, pady=20)
        self.discount_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def set_discount(self, percent):
        """Set discount percentage"""
        self.discount_percent.set(percent)
    
    def calculate_discount(self):
        """Calculate discount results"""
        try:
            original = self.original_price.get()
            discount = self.discount_percent.get()
            
            if original <= 0:
                messagebox.showerror("Error", "Please enter a valid price")
                return
            
            discount_amount = original * (discount / 100)
            sale_price = original - discount_amount
            
            # Clear previous results
            for widget in self.discount_results_frame.winfo_children():
                widget.destroy()
            
            # Display results
            results_text = f"""
            🛍️ DISCOUNT CALCULATOR 🛍️
            {"="*40}
            
            Original Price:   ${original:.2f}
            Discount:         {discount}%
            {"-"*40}
            You Save:         ${discount_amount:.2f}
            Sale Price:       ${sale_price:.2f}
            {"="*40}
            
            💰 You save {discount_amount/original*100:.1f}% of the original price!
            """
            
            result_label = tk.Label(self.discount_results_frame, text=results_text,
                                   font=("Courier", 11), bg=self.colors['light'],
                                   justify="left")
            result_label.pack(pady=10)
            
            # Add to history
            self.history.append(f"Discount: ${original:.2f} → ${sale_price:.2f} ({discount}% off)")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def create_percentage_tab(self):
        """Create Percentage Change tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📈 Percentage")
        
        input_frame = tk.LabelFrame(tab, text="Input Values", font=("Arial", 12, "bold"),
                                   bg=self.colors['light'], padx=20, pady=20)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Old value
        tk.Label(input_frame, text="Original Value:", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.old_value = tk.DoubleVar(value=100.0)
        tk.Entry(input_frame, textvariable=self.old_value, font=("Arial", 11),
                width=20).grid(row=0, column=1, pady=5, padx=5)
        
        # New value
        tk.Label(input_frame, text="New Value:", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.new_value = tk.DoubleVar(value=120.0)
        tk.Entry(input_frame, textvariable=self.new_value, font=("Arial", 11),
                width=20).grid(row=1, column=1, pady=5, padx=5)
        
        # Calculate button
        calc_btn = tk.Button(input_frame, text="📊 Calculate Change", command=self.calculate_percentage,
                           bg=self.colors['primary'], fg="white", font=("Arial", 11, "bold"),
                           padx=20, pady=10)
        calc_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Results frame
        self.percentage_results_frame = tk.LabelFrame(tab, text="Results", font=("Arial", 12, "bold"),
                                                     bg=self.colors['light'], padx=20, pady=20)
        self.percentage_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def calculate_percentage(self):
        """Calculate percentage change"""
        try:
            old_val = self.old_value.get()
            new_val = self.new_value.get()
            
            if old_val == 0:
                messagebox.showerror("Error", "Original value cannot be zero")
                return
            
            change = new_val - old_val
            percent_change = (change / abs(old_val)) * 100
            change_type = "INCREASE" if change > 0 else "DECREASE" if change < 0 else "NO CHANGE"
            
            # Clear previous results
            for widget in self.percentage_results_frame.winfo_children():
                widget.destroy()
            
            # Color based on change
            color = self.colors['success'] if change > 0 else self.colors['danger'] if change < 0 else self.colors['dark']
            
            # Display results
            results_text = f"""
            📈 PERCENTAGE CHANGE 📈
            {"="*40}
            
            Original Value:   {old_val:,.2f}
            New Value:        {new_val:,.2f}
            {"-"*40}
            Change Amount:    {abs(change):,.2f}
            Percentage:       {abs(percent_change):.2f}%
            Change Type:      {change_type}
            {"="*40}
            """
            
            result_label = tk.Label(self.percentage_results_frame, text=results_text,
                                   font=("Courier", 11), bg=self.colors['light'],
                                   fg=color, justify="left")
            result_label.pack(pady=10)
            
            # Add to history
            self.history.append(f"Percentage: {old_val} → {new_val} = {percent_change:.1f}% {change_type.lower()}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def create_gpa_tab(self):
        """Create GPA Calculator tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏫 GPA Calculator")
        
        # Course entry frame
        entry_frame = tk.LabelFrame(tab, text="Add Courses", font=("Arial", 12, "bold"),
                                   bg=self.colors['light'], padx=20, pady=20)
        entry_frame.pack(fill="x", padx=10, pady=10)
        
        # Course name
        tk.Label(entry_frame, text="Course Name:", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.course_name = tk.StringVar()
        tk.Entry(entry_frame, textvariable=self.course_name, font=("Arial", 11),
                width=20).grid(row=0, column=1, pady=5, padx=5)
        
        # Grade
        tk.Label(entry_frame, text="Grade:", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.grade = tk.StringVar(value="A")
        grade_combo = ttk.Combobox(entry_frame, textvariable=self.grade,
                                  values=["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"],
                                  width=17, state="readonly")
        grade_combo.grid(row=1, column=1, pady=5, padx=5)
        
        # Credits
        tk.Label(entry_frame, text="Credits:", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
        self.credits = tk.DoubleVar(value=3.0)
        tk.Spinbox(entry_frame, from_=0.5, to=10, increment=0.5, textvariable=self.credits,
                  font=("Arial", 11), width=10).grid(row=2, column=1, pady=5, padx=5)
        
        # Add course button
        add_btn = tk.Button(entry_frame, text="➕ Add Course", command=self.add_course,
                          bg=self.colors['primary'], fg="white", font=("Arial", 10, "bold"))
        add_btn.grid(row=3, column=0, pady=10)
        
        # Calculate button
        calc_btn = tk.Button(entry_frame, text="🧮 Calculate GPA", command=self.calculate_gpa,
                           bg=self.colors['success'], fg="white", font=("Arial", 10, "bold"))
        calc_btn.grid(row=3, column=1, pady=10)
        
        # Courses list frame
        list_frame = tk.LabelFrame(tab, text="Current Courses", font=("Arial", 12, "bold"),
                                  bg=self.colors['light'], padx=20, pady=20)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview for courses
        columns = ("Course", "Grade", "Credits", "Points")
        self.courses_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.courses_tree.heading(col, text=col)
            self.courses_tree.column(col, width=100)
        
        self.courses_tree.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.courses_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.courses_tree.configure(yscrollcommand=scrollbar.set)
        
        # Remove selected button
        remove_btn = tk.Button(list_frame, text="🗑️ Remove Selected", command=self.remove_course,
                             bg=self.colors['danger'], fg="white", font=("Arial", 10, "bold"))
        remove_btn.pack(pady=5)
        
        # Clear all button
        clear_btn = tk.Button(list_frame, text="🗑️ Clear All", command=self.clear_courses,
                            bg=self.colors['warning'], fg="white", font=("Arial", 10, "bold"))
        clear_btn.pack(pady=5)
        
        # Results frame
        self.gpa_results_frame = tk.LabelFrame(tab, text="GPA Results", font=("Arial", 12, "bold"),
                                              bg=self.colors['light'], padx=20, pady=20)
        self.gpa_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize courses list
        self.courses_list = []
    
    def add_course(self):
        """Add a course to the list"""
        name = self.course_name.get().strip()
        grade = self.grade.get()
        credits = self.credits.get()
        
        if not name:
            messagebox.showerror("Error", "Please enter a course name")
            return
        
        # Grade points mapping
        grade_points = {
            'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'F': 0.0
        }
        
        points = grade_points.get(grade, 0.0)
        
        # Add to treeview
        self.courses_tree.insert("", "end", values=(name, grade, credits, points))
        
        # Add to internal list
        self.courses_list.append({
            'name': name,
            'grade': grade,
            'credits': credits,
            'points': points
        })
        
        # Clear input fields
        self.course_name.set("")
        self.grade.set("A")
        self.credits.set(3.0)
    
    def remove_course(self):
        """Remove selected course"""
        selected_item = self.courses_tree.selection()
        if selected_item:
            # Find and remove from internal list
            item_values = self.courses_tree.item(selected_item)['values']
            self.courses_list = [c for c in self.courses_list if not (
                c['name'] == item_values[0] and 
                c['grade'] == item_values[1] and 
                c['credits'] == item_values[2]
            )]
            
            # Remove from treeview
            self.courses_tree.delete(selected_item)
    
    def clear_courses(self):
        """Clear all courses"""
        if messagebox.askyesno("Confirm", "Clear all courses?"):
            self.courses_tree.delete(*self.courses_tree.get_children())
            self.courses_list.clear()
    
    def calculate_gpa(self):
        """Calculate GPA from courses"""
        if not self.courses_list:
            messagebox.showwarning("No Courses", "Please add courses first")
            return
        
        total_credits = sum(course['credits'] for course in self.courses_list)
        total_quality_points = sum(course['points'] * course['credits'] for course in self.courses_list)
        
        if total_credits == 0:
            messagebox.showerror("Error", "Total credits cannot be zero")
            return
        
        gpa = total_quality_points / total_credits
        
        # Clear previous results
        for widget in self.gpa_results_frame.winfo_children():
            widget.destroy()
        
        # Determine letter equivalent
        if gpa >= 3.7:
            letter = "A-/A"
        elif gpa >= 3.3:
            letter = "B+"
        elif gpa >= 3.0:
            letter = "B"
        elif gpa >= 2.7:
            letter = "B-"
        elif gpa >= 2.3:
            letter = "C+"
        elif gpa >= 2.0:
            letter = "C"
        elif gpa >= 1.7:
            letter = "C-"
        elif gpa >= 1.0:
            letter = "D"
        else:
            letter = "F"
        
        # Display results
        results_text = f"""
        🏫 GPA CALCULATOR RESULTS 🏫
        {"="*40}
        
        Total Courses:      {len(self.courses_list)}
        Total Credits:      {total_credits:.1f}
        {"-"*40}
        Your GPA:           {gpa:.3f}
        Letter Equivalent:  {letter}
        {"="*40}
        
        📊 Grade Scale:
        A = 4.0, A- = 3.7, B+ = 3.3, B = 3.0
        B- = 2.7, C+ = 2.3, C = 2.0, C- = 1.7
        D = 1.0, F = 0.0
        """
        
        result_label = tk.Label(self.gpa_results_frame, text=results_text,
                               font=("Courier", 11), bg=self.colors['light'],
                               justify="left")
        result_label.pack(pady=10)
        
        # Add to history
        self.history.append(f"GPA: {gpa:.3f} from {len(self.courses_list)} courses")
    
    def create_tax_tab(self):
        """Create Sales Tax Calculator tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💰 Tax")
        
        input_frame = tk.LabelFrame(tab, text="Input Parameters", font=("Arial", 12, "bold"),
                                   bg=self.colors['light'], padx=20, pady=20)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Price
        tk.Label(input_frame, text="Item Price ($):", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.item_price = tk.DoubleVar(value=100.0)
        tk.Entry(input_frame, textvariable=self.item_price, font=("Arial", 11),
                width=20).grid(row=0, column=1, pady=5, padx=5)
        
        # Tax rate
        tk.Label(input_frame, text="Tax Rate (%):", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.tax_rate = tk.DoubleVar(value=8.25)
        tk.Entry(input_frame, textvariable=self.tax_rate, font=("Arial", 11),
                width=20).grid(row=1, column=1, pady=5, padx=5)
        
        # Common rates buttons
        button_frame = tk.Frame(input_frame, bg=self.colors['light'])
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        rates = [("CA: 7.25%", 7.25), ("NY: 8.875%", 8.875), 
                ("TX: 6.25%", 6.25), ("FL: 6.0%", 6.0)]
        
        for i, (label, rate) in enumerate(rates):
            btn = tk.Button(button_frame, text=label, width=12,
                          command=lambda r=rate: self.set_tax_rate(r),
                          bg=self.colors['primary'], fg="white")
            btn.grid(row=0, column=i, padx=2)
        
        # Calculate button
        calc_btn = tk.Button(input_frame, text="🧾 Calculate Tax", command=self.calculate_tax,
                           bg=self.colors['primary'], fg="white", font=("Arial", 11, "bold"),
                           padx=20, pady=10)
        calc_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Results frame
        self.tax_results_frame = tk.LabelFrame(tab, text="Results", font=("Arial", 12, "bold"),
                                              bg=self.colors['light'], padx=20, pady=20)
        self.tax_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def set_tax_rate(self, rate):
        """Set tax rate"""
        self.tax_rate.set(rate)
    
    def calculate_tax(self):
        """Calculate sales tax"""
        try:
            price = self.item_price.get()
            tax_rate = self.tax_rate.get()
            
            if price <= 0:
                messagebox.showerror("Error", "Please enter a valid price")
                return
            
            tax_amount = price * (tax_rate / 100)
            total_price = price + tax_amount
            
            # Clear previous results
            for widget in self.tax_results_frame.winfo_children():
                widget.destroy()
            
            # Display results
            results_text = f"""
            💰 SALES TAX CALCULATOR 💰
            {"="*40}
            
            Item Price:       ${price:.2f}
            Tax Rate:         {tax_rate}%
            {"-"*40}
            Tax Amount:       ${tax_amount:.2f}
            Total Price:      ${total_price:.2f}
            {"="*40}
            """
            
            result_label = tk.Label(self.tax_results_frame, text=results_text,
                                   font=("Courier", 11), bg=self.colors['light'],
                                   justify="left")
            result_label.pack(pady=10)
            
            # Add to history
            self.history.append(f"Tax: ${price:.2f} + {tax_rate}% = ${total_price:.2f}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def create_interest_tab(self):
        """Create Compound Interest tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💹 Interest")
        
        input_frame = tk.LabelFrame(tab, text="Input Parameters", font=("Arial", 12, "bold"),
                                   bg=self.colors['light'], padx=20, pady=20)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Principal
        tk.Label(input_frame, text="Principal Amount ($):", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.principal = tk.DoubleVar(value=1000.0)
        tk.Entry(input_frame, textvariable=self.principal, font=("Arial", 11),
                width=20).grid(row=0, column=1, pady=5, padx=5)
        
        # Annual rate
        tk.Label(input_frame, text="Annual Rate (%):", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.annual_rate = tk.DoubleVar(value=5.0)
        tk.Entry(input_frame, textvariable=self.annual_rate, font=("Arial", 11),
                width=20).grid(row=1, column=1, pady=5, padx=5)
        
        # Years
        tk.Label(input_frame, text="Years:", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
        self.years = tk.IntVar(value=10)
        tk.Spinbox(input_frame, from_=1, to=50, textvariable=self.years,
                  font=("Arial", 11), width=10).grid(row=2, column=1, pady=5, padx=5)
        
        # Monthly contribution
        tk.Label(input_frame, text="Monthly Contribution ($):", bg=self.colors['light'],
                font=("Arial", 11)).grid(row=3, column=0, sticky="w", pady=5)
        self.monthly_contrib = tk.DoubleVar(value=0.0)
        tk.Entry(input_frame, textvariable=self.monthly_contrib, font=("Arial", 11),
                width=20).grid(row=3, column=1, pady=5, padx=5)
        
        # Calculate button
        calc_btn = tk.Button(input_frame, text="📈 Calculate Interest", command=self.calculate_interest,
                           bg=self.colors['primary'], fg="white", font=("Arial", 11, "bold"),
                           padx=20, pady=10)
        calc_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Results frame
        self.interest_results_frame = tk.LabelFrame(tab, text="Results", font=("Arial", 12, "bold"),
                                                   bg=self.colors['light'], padx=20, pady=20)
        self.interest_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def calculate_interest(self):
        """Calculate compound interest"""
        try:
            principal = self.principal.get()
            rate = self.annual_rate.get()
            years = self.years.get()
            monthly = self.monthly_contrib.get()
            
            if principal <= 0 or rate < 0 or years <= 0 or monthly < 0:
                messagebox.showerror("Error", "Please enter valid positive values")
                return
            
            # Monthly compounding
            monthly_rate = rate / 100 / 12
            months = years * 12
            
            # Future value of principal
            future_value = principal * ((1 + monthly_rate) ** months)
            
            # Future value of monthly contributions
            if monthly > 0:
                annuity_factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
                future_value += monthly * annuity_factor
            
            total_contributions = principal + (monthly * months)
            interest_earned = future_value - total_contributions
            
            # Clear previous results
            for widget in self.interest_results_frame.winfo_children():
                widget.destroy()
            
            # Display results
            results_text = f"""
            💹 COMPOUND INTEREST CALCULATOR 💹
            {"="*50}
            
            Principal Amount:      ${principal:,.2f}
            Annual Rate:           {rate}%
            Time Period:           {years} years
            Monthly Contribution:  ${monthly:,.2f}
            {"-"*50}
            Total Contributions:   ${total_contributions:,.2f}
            Interest Earned:       ${interest_earned:,.2f}
            Future Value:          ${future_value:,.2f}
            {"="*50}
            
            📊 Summary:
            • Your money grows by ${interest_earned:,.2f}
            • That's {interest_earned/principal*100:.1f}% growth
            """
            
            result_label = tk.Label(self.interest_results_frame, text=results_text,
                                   font=("Courier", 11), bg=self.colors['light'],
                                   justify="left")
            result_label.pack(pady=10)
            
            # Add to history
            self.history.append(f"Interest: ${principal:.0f} at {rate}% for {years} years = ${future_value:,.2f}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def create_history_tab(self):
        """Create History tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📜 History")
        
        # Title
        title_label = tk.Label(tab, text="📜 Calculation History", 
                              font=("Arial", 16, "bold"), bg=self.colors['light'])
        title_label.pack(pady=10)
        
        # History display (scrolled text)
        self.history_text = scrolledtext.ScrolledText(tab, width=80, height=25,
                                                     font=("Courier", 10))
        self.history_text.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Buttons frame
        button_frame = tk.Frame(tab, bg=self.colors['light'])
        button_frame.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(button_frame, text="🔄 Refresh History",
                              command=self.refresh_history,
                              bg=self.colors['primary'], fg="white",
                              font=("Arial", 10, "bold"), padx=15, pady=8)
        refresh_btn.grid(row=0, column=0, padx=5)
        
        # Clear history button
        clear_btn = tk.Button(button_frame, text="🗑️ Clear History",
                            command=self.clear_all_history,
                            bg=self.colors['danger'], fg="white",
                            font=("Arial", 10, "bold"), padx=15, pady=8)
        clear_btn.grid(row=0, column=1, padx=5)
        
        # Export button
        export_btn = tk.Button(button_frame, text="💾 Export to File",
                              command=self.export_history,
                              bg=self.colors['success'], fg="white",
                              font=("Arial", 10, "bold"), padx=15, pady=8)
        export_btn.grid(row=0, column=2, padx=5)
        
        # Initial refresh
        self.refresh_history()
    
    def refresh_history(self):
        """Refresh history display"""
        self.history_text.delete(1.0, tk.END)
        
        if not self.history:
            self.history_text.insert(tk.END, "No calculations yet.\n")
            self.history_text.insert(tk.END, "Perform calculations in other tabs to see them here.")
        else:
            for i, entry in enumerate(reversed(self.history), 1):
                self.history_text.insert(tk.END, f"{i}. {entry}\n")
    
    def clear_all_history(self):
        """Clear all history"""
        if messagebox.askyesno("Confirm", "Clear all calculation history?"):
            self.history.clear()
            self.refresh_history()
    
    def export_history(self):
        """Export history to file"""
        if not self.history:
            messagebox.showwarning("No Data", "No calculations to export")
            return
        
        try:
            with open("calculator_history.txt", "w") as f:
                f.write("Data Calculator History\n")
                f.write("=" * 50 + "\n\n")
                for i, entry in enumerate(self.history, 1):
                    f.write(f"{i}. {entry}\n")
            
            messagebox.showinfo("Success", "History exported to calculator_history.txt")
        except:
            messagebox.showerror("Error", "Could not export history")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = DataCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
