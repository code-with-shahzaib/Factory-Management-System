import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from database import *
from models import *
import webbrowser
import os
from PIL import Image, ImageTk
from itertools import cycle
import time
from jinja2 import Template


class FactoryManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Premax Factory Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f5f5f5')
        
        # Center the window
        self.center_window()
        
        # Modern style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom colors
        self.primary_color = '#3498db'
        self.secondary_color = '#2980b9'
        self.accent_color = '#e74c3c'
        self.light_color = '#ecf0f1'
        self.dark_color = '#2c3e50'
        
        # Configure styles
        self.style.configure('TFrame', background=self.light_color)
        self.style.configure('TLabel', background=self.light_color, font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=8)
        self.style.configure('Primary.TButton', background=self.primary_color, foreground='white')
        self.style.configure('Secondary.TButton', background=self.secondary_color, foreground='white')
        self.style.configure('Accent.TButton', background=self.accent_color, foreground='white')
        self.style.configure('Dark.TButton', background=self.dark_color, foreground='white')
        
        # Create welcome screen
        self.create_welcome_screen()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def clear_frame(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_welcome_screen(self):
        """Create animated welcome screen"""
        self.clear_frame()
        
        # Main container
        welcome_frame = tk.Frame(self.root, bg=self.dark_color)
        welcome_frame.pack(expand=True, fill='both')
        
        # Logo and title
        logo_frame = tk.Frame(welcome_frame, bg=self.dark_color)
        logo_frame.pack(pady=100)
        
        # Try to load logo image
        try:
            logo_img = Image.open("images/logo.png")
            logo_img = logo_img.resize((200, 200), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(logo_frame, image=self.logo, bg=self.dark_color)
            logo_label.pack()
        except Exception as e:
            # Fallback text logo
            logo_label = tk.Label(logo_frame, text="🏭", font=('Arial', 80), 
                                bg=self.dark_color, fg='white')
            logo_label.pack()
        
        # App title
        title_label = tk.Label(logo_frame, text="Premax Factory Management", 
                             font=('Segoe UI', 24, 'bold'), bg=self.dark_color, fg='white')
        title_label.pack(pady=20)
        
        # Loading animation
        loading_frame = tk.Frame(welcome_frame, bg=self.dark_color)
        loading_frame.pack(pady=50)
        
        loading_text = tk.Label(loading_frame, text="Loading...", 
                              font=('Segoe UI', 12), bg=self.dark_color, fg='white')
        loading_text.pack()
        
        # Animated dots
        self.dots = cycle(['.', '..', '...'])
        self.loading_dots = tk.Label(loading_frame, text="", 
                                    font=('Segoe UI', 12), bg=self.dark_color, fg='white')
        self.loading_dots.pack()
        
        # Progress bar
        progress = ttk.Progressbar(welcome_frame, orient='horizontal', 
                                 length=300, mode='determinate')
        progress.pack(pady=20)
        
        # Copyright
        copyright_label = tk.Label(welcome_frame, 
                                 text="© 2025 Premax Factory Management System", 
                                 font=('Segoe UI', 8), bg=self.dark_color, fg='white')
        copyright_label.pack(side='bottom', pady=20)
        
        # Animate loading
        self.animate_loading(progress, welcome_frame)
    
    def animate_loading(self, progress, welcome_frame):
        """Animate loading screen"""
        if progress['value'] < 100:
            progress['value'] += 5
            self.loading_dots.config(text=next(self.dots))
            self.root.after(100, lambda: self.animate_loading(progress, welcome_frame))
        else:
            self.root.after(500, lambda: self.create_main_menu())
    
    def create_main_menu(self):
        """Create beautiful main menu"""
        self.clear_frame()
        
        # Main container with gradient background
        main_frame = tk.Frame(self.root, bg=self.light_color)
        main_frame.pack(expand=True, fill='both')
        
        # Header with logo and title
        header = tk.Frame(main_frame, bg=self.dark_color)
        header.pack(fill='x', pady=(0, 30))
        
        # Logo and title
        logo_title_frame = tk.Frame(header, bg=self.dark_color)
        logo_title_frame.pack(pady=20)
        
        # Try to load small logo
        try:
            small_logo_img = Image.open("images/logo.png")
            small_logo_img = small_logo_img.resize((50, 50), Image.LANCZOS)
            self.small_logo = ImageTk.PhotoImage(small_logo_img)
            logo_label = tk.Label(logo_title_frame, image=self.small_logo, bg=self.dark_color)
            logo_label.pack(side='left', padx=10)
        except:
            # Fallback text logo
            logo_label = tk.Label(logo_title_frame, text="🏭", font=('Arial', 24), 
                                bg=self.dark_color, fg='white')
            logo_label.pack(side='left', padx=10)
        
        # Title
        title_label = tk.Label(logo_title_frame, text="Factory Management System", 
                             font=('Segoe UI', 20, 'bold'), bg=self.dark_color, fg='white')
        title_label.pack(side='left')
        
        # Menu buttons container
        menu_frame = tk.Frame(main_frame, bg=self.light_color)
        menu_frame.pack(expand=True, padx=100, pady=20)
        
        # Menu buttons with icons
        menu_items = [
            ("👨‍🏭 Workers", self.show_workers_management),
            ("🎨 Designs", self.show_designs_management),
            ("📊 Production", self.show_production_tracking),
            ("👥 Clients", self.show_clients_management),
            ("📦 Orders", self.show_orders_management),
            ("🧾 Invoices", self.show_invoices_management),
            ("💰 Reports", self.show_salary_reports),
            ("🚪 Exit", self.root.quit)
        ]
        
        # Create stylish buttons
        for i, (text, command) in enumerate(menu_items):
            btn = ttk.Button(menu_frame, text=text, command=command, 
                           style='Primary.TButton', width=20)
            btn.grid(row=i//2, column=i%2, padx=15, pady=15, sticky='nsew')
        
        # Configure grid
        for i in range(2):
            menu_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            menu_frame.grid_rowconfigure(i, weight=1)
        
        # Footer
        footer = tk.Frame(main_frame, bg=self.dark_color, height=40)
        footer.pack(fill='x', side='bottom')
        
        user_label = tk.Label(footer, text=f"Welcome, Admin", 
                            font=('Segoe UI', 9), bg=self.dark_color, fg='white')
        user_label.pack(side='left', padx=20)
        
        date_label = tk.Label(footer, text=datetime.now().strftime('%Y-%m-%d %H:%M'), 
                            font=('Segoe UI', 9), bg=self.dark_color, fg='white')
        date_label.pack(side='right', padx=20)

    # ==================== WORKERS MANAGEMENT ====================
    def show_workers_management(self):
        self.clear_frame()
        
        # Header
        header = tk.Frame(self.root, bg=self.dark_color)
        header.pack(fill='x')
        tk.Label(header, text="Workers Management", font=('Segoe UI', 18, 'bold'), 
                fg='white', bg=self.dark_color).pack(pady=10)
        
        main_frame = tk.Frame(self.root, bg=self.light_color)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Left Frame - Form
        left_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        left_frame.pack(side='left', fill='y')
        
        tk.Label(left_frame, text="Add/Edit Worker", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        form_frame = tk.Frame(left_frame, bg=self.light_color)
        form_frame.pack(pady=10)
        
        labels = ["Name:", "Contact:", "Joining Date (YYYY-MM-DD):", "Hourly Rate:"]
        self.worker_entries = []
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg=self.light_color).grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = ttk.Entry(form_frame, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.worker_entries.append(entry)
        
        button_frame = tk.Frame(left_frame, bg=self.light_color)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Worker", command=self.add_worker, 
                 style='Success.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Worker", command=self.update_worker, 
                 style='Warning.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Worker", command=self.delete_worker, 
                 style='Danger.TButton').grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_worker_form, 
                 style='Primary.TButton').grid(row=0, column=3, padx=5)
        
        # Right Frame - List
        right_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        right_frame.pack(side='right', expand=True, fill='both')
        
        tk.Label(right_frame, text="Workers List", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        # Treeview
        self.workers_tree = ttk.Treeview(right_frame, columns=("ID", "Name", "Contact", "Joining Date", "Hourly Rate"), 
                                       show='headings', selectmode='browse')
        
        self.workers_tree.heading("ID", text="ID")
        self.workers_tree.heading("Name", text="Name")
        self.workers_tree.heading("Contact", text="Contact")
        self.workers_tree.heading("Joining Date", text="Joining Date")
        self.workers_tree.heading("Hourly Rate", text="Hourly Rate")
        
        self.workers_tree.column("ID", width=50, anchor='center')
        self.workers_tree.column("Name", width=150)
        self.workers_tree.column("Contact", width=120)
        self.workers_tree.column("Joining Date", width=100, anchor='center')
        self.workers_tree.column("Hourly Rate", width=80, anchor='e')
        
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.workers_tree.yview)
        self.workers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.workers_tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.workers_tree.bind('<<TreeviewSelect>>', self.on_worker_select)
        
        # Load data
        self.load_workers()
        
        # Home button
        home_btn = ttk.Button(main_frame, text="🏠 Home", command=self.create_main_menu,
                            style='Dark.TButton')
        home_btn.pack(side='bottom', pady=10)
    
    def load_workers(self):
        for item in self.workers_tree.get_children():
            self.workers_tree.delete(item)
        
        workers = get_all_workers()
        for worker in workers:
            self.workers_tree.insert('', 'end', values=worker)
    
    def add_worker(self):
        name = self.worker_entries[0].get()
        contact = self.worker_entries[1].get()
        joining_date = self.worker_entries[2].get()
        hourly_rate = self.worker_entries[3].get()
        
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return
        
        try:
            hourly_rate = float(hourly_rate) if hourly_rate else 0
        except ValueError:
            messagebox.showerror("Error", "Invalid hourly rate!")
            return
        
        # Validate date format
        if joining_date:
            try:
                datetime.strptime(joining_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO workers (name, contact, joining_date, hourly_rate) VALUES (?, ?, ?, ?)",
            (name, contact, joining_date, hourly_rate)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Worker added successfully!")
        self.load_workers()
        self.clear_worker_form()
    
    def update_worker(self):
        selected = self.workers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a worker to update!")
            return
        
        worker_id = self.workers_tree.item(selected[0])['values'][0]
        name = self.worker_entries[0].get()
        contact = self.worker_entries[1].get()
        joining_date = self.worker_entries[2].get()
        hourly_rate = self.worker_entries[3].get()
        
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return
        
        try:
            hourly_rate = float(hourly_rate) if hourly_rate else 0
        except ValueError:
            messagebox.showerror("Error", "Invalid hourly rate!")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE workers SET name=?, contact=?, joining_date=?, hourly_rate=? WHERE id=?",
            (name, contact, joining_date, hourly_rate, worker_id)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Worker updated successfully!")
        self.load_workers()
    
    def delete_worker(self):
        selected = self.workers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a worker to delete!")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this worker?"):
            return
        
        worker_id = self.workers_tree.item(selected[0])['values'][0]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM workers WHERE id=?", (worker_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Worker deleted successfully!")
        self.load_workers()
        self.clear_worker_form()
    
    def clear_worker_form(self):
        for entry in self.worker_entries:
            entry.delete(0, tk.END)
    
    def on_worker_select(self, event):
        selected = self.workers_tree.selection()
        if not selected:
            return
        
        worker_data = self.workers_tree.item(selected[0])['values']
        self.clear_worker_form()
        
        for i, value in enumerate(worker_data[1:]):  # Skip ID
            self.worker_entries[i].insert(0, str(value) if value is not None else "")

    # ==================== DESIGNS MANAGEMENT ====================
    def show_designs_management(self):
        self.clear_frame()
        
        header = tk.Frame(self.root, bg=self.dark_color)
        header.pack(fill='x')
        tk.Label(header, text="Designs Management", font=('Segoe UI', 18, 'bold'), 
                fg='white', bg=self.dark_color).pack(pady=10)
        
        main_frame = tk.Frame(self.root, bg=self.light_color)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Left Frame - Form
        left_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        left_frame.pack(side='left', fill='y')
        
        tk.Label(left_frame, text="Add/Edit Design", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        form_frame = tk.Frame(left_frame, bg=self.light_color)
        form_frame.pack(pady=10)
        
        labels = ["Name:", "Description:", "Base Price:", "Complexity Level (1-5):"]
        self.design_entries = []
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg=self.light_color).grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = ttk.Entry(form_frame, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.design_entries.append(entry)
        
        button_frame = tk.Frame(left_frame, bg=self.light_color)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Design", command=self.add_design, 
                 style='Success.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Design", command=self.update_design, 
                 style='Warning.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Design", command=self.delete_design, 
                 style='Danger.TButton').grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_design_form, 
                 style='Primary.TButton').grid(row=0, column=3, padx=5)
        
        # Right Frame - List
        right_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        right_frame.pack(side='right', expand=True, fill='both')
        
        tk.Label(right_frame, text="Designs List", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        # Treeview
        self.designs_tree = ttk.Treeview(right_frame, columns=("ID", "Name", "Description", "Base Price", "Complexity"), 
                                       show='headings', selectmode='browse')
        
        self.designs_tree.heading("ID", text="ID")
        self.designs_tree.heading("Name", text="Name")
        self.designs_tree.heading("Description", text="Description")
        self.designs_tree.heading("Base Price", text="Base Price")
        self.designs_tree.heading("Complexity", text="Complexity")
        
        self.designs_tree.column("ID", width=50, anchor='center')
        self.designs_tree.column("Name", width=150)
        self.designs_tree.column("Description", width=200)
        self.designs_tree.column("Base Price", width=80, anchor='e')
        self.designs_tree.column("Complexity", width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.designs_tree.yview)
        self.designs_tree.configure(yscrollcommand=scrollbar.set)
        
        self.designs_tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.designs_tree.bind('<<TreeviewSelect>>', self.on_design_select)
        
        # Load data
        self.load_designs()
        
        # Home button
        home_btn = ttk.Button(main_frame, text="🏠 Home", command=self.create_main_menu,
                            style='Dark.TButton')
        home_btn.pack(side='bottom', pady=10)
    
    def load_designs(self):
        for item in self.designs_tree.get_children():
            self.designs_tree.delete(item)
        
        designs = get_all_designs()
        for design in designs:
            self.designs_tree.insert('', 'end', values=design)
    
    def add_design(self):
        name = self.design_entries[0].get()
        description = self.design_entries[1].get()
        base_price = self.design_entries[2].get()
        complexity = self.design_entries[3].get()
        
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return
        
        try:
            base_price = float(base_price) if base_price else 0
        except ValueError:
            messagebox.showerror("Error", "Invalid base price!")
            return
        
        try:
            complexity = int(complexity) if complexity else 1
            if complexity < 1 or complexity > 5:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Complexity must be between 1 and 5!")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO designs (name, description, base_price, complexity_level) VALUES (?, ?, ?, ?)",
            (name, description, base_price, complexity)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Design added successfully!")
        self.load_designs()
        self.clear_design_form()
    
    def update_design(self):
        selected = self.designs_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a design to update!")
            return
        
        design_id = self.designs_tree.item(selected[0])['values'][0]
        name = self.design_entries[0].get()
        description = self.design_entries[1].get()
        base_price = self.design_entries[2].get()
        complexity = self.design_entries[3].get()
        
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return
        
        try:
            base_price = float(base_price) if base_price else 0
        except ValueError:
            messagebox.showerror("Error", "Invalid base price!")
            return
        
        try:
            complexity = int(complexity) if complexity else 1
            if complexity < 1 or complexity > 5:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Complexity must be between 1 and 5!")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE designs SET name=?, description=?, base_price=?, complexity_level=? WHERE id=?",
            (name, description, base_price, complexity, design_id)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Design updated successfully!")
        self.load_designs()
    
    def delete_design(self):
        selected = self.designs_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a design to delete!")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this design?"):
            return
        
        design_id = self.designs_tree.item(selected[0])['values'][0]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM designs WHERE id=?", (design_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Design deleted successfully!")
        self.load_designs()
        self.clear_design_form()
    
    def clear_design_form(self):
        for entry in self.design_entries:
            entry.delete(0, tk.END)
    
    def on_design_select(self, event):
        selected = self.designs_tree.selection()
        if not selected:
            return
        
        design_data = self.designs_tree.item(selected[0])['values']
        self.clear_design_form()
        
        for i, value in enumerate(design_data[1:]):  # Skip ID
            if i < len(self.design_entries):  # Ensure we don't exceed entries
                self.design_entries[i].delete(0, tk.END)
                self.design_entries[i].insert(0, str(value) if value is not None else "")

    # ==================== PRODUCTION TRACKING ====================
    def show_production_tracking(self):
        self.clear_frame()
        
        header = tk.Frame(self.root, bg=self.dark_color)
        header.pack(fill='x')
        tk.Label(header, text="Production Tracking", font=('Segoe UI', 18, 'bold'), 
                fg='white', bg=self.dark_color).pack(pady=10)
        
        main_frame = tk.Frame(self.root, bg=self.light_color)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Left Frame - Form
        left_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        left_frame.pack(side='left', fill='y')
        
        tk.Label(left_frame, text="Add Production Record", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        form_frame = tk.Frame(left_frame, bg=self.light_color)
        form_frame.pack(pady=10)
        
        # Worker dropdown
        tk.Label(form_frame, text="Worker:", bg=self.light_color).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.worker_var = tk.StringVar()
        self.worker_dropdown = ttk.Combobox(form_frame, textvariable=self.worker_var, state='readonly', width=23)
        self.worker_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        # Design dropdown
        tk.Label(form_frame, text="Design:", bg=self.light_color).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.design_var = tk.StringVar()
        self.design_dropdown = ttk.Combobox(form_frame, textvariable=self.design_var, state='readonly', width=23)
        self.design_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        # Quantity
        tk.Label(form_frame, text="Quantity:", bg=self.light_color).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.quantity_entry = ttk.Entry(form_frame, width=25)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Date
        tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg=self.light_color).grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.date_entry = ttk.Entry(form_frame, width=25)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)
        
        button_frame = tk.Frame(left_frame, bg=self.light_color)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Record", command=self.add_production_record, 
                 style='Success.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Delete Record", command=self.delete_production_record, 
                 style='Danger.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_production_form, 
                 style='Primary.TButton').grid(row=0, column=2, padx=5)
        
        # Right Frame - List
        right_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        right_frame.pack(side='right', expand=True, fill='both')
        
        tk.Label(right_frame, text="Production Records", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        # Treeview
        self.production_tree = ttk.Treeview(right_frame, columns=("ID", "Worker", "Design", "Quantity", "Date"), 
                                          show='headings', selectmode='browse')
        
        self.production_tree.heading("ID", text="ID")
        self.production_tree.heading("Worker", text="Worker")
        self.production_tree.heading("Design", text="Design")
        self.production_tree.heading("Quantity", text="Quantity")
        self.production_tree.heading("Date", text="Date")
        
        self.production_tree.column("ID", width=50, anchor='center')
        self.production_tree.column("Worker", width=150)
        self.production_tree.column("Design", width=150)
        self.production_tree.column("Quantity", width=80, anchor='center')
        self.production_tree.column("Date", width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.production_tree.yview)
        self.production_tree.configure(yscrollcommand=scrollbar.set)
        
        self.production_tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.production_tree.bind('<<TreeviewSelect>>', self.on_production_select)
        
        # Load dropdowns and data
        self.load_production_dropdowns()
        self.load_production_records()
        
        # Home button
        home_btn = ttk.Button(main_frame, text="🏠 Home", command=self.create_main_menu,
                            style='Dark.TButton')
        home_btn.pack(side='bottom', pady=10)
    
    def load_production_dropdowns(self):
        workers = get_all_workers()
        worker_options = [f"{w[0]} - {w[1]}" for w in workers]
        self.worker_dropdown['values'] = worker_options
        
        designs = get_all_designs()
        design_options = [f"{d[0]} - {d[1]}" for d in designs]
        self.design_dropdown['values'] = design_options
    
    def load_production_records(self):
        for item in self.production_tree.get_children():
            self.production_tree.delete(item)
        
        records = get_production_records()
        for record in records:
            self.production_tree.insert('', 'end', values=record)
    
    def add_production_record(self):
        worker = self.worker_var.get()
        design = self.design_var.get()
        quantity = self.quantity_entry.get()
        date = self.date_entry.get()
        
        if not worker or not design:
            messagebox.showerror("Error", "Please select both worker and design!")
            return
        
        try:
            worker_id = int(worker.split(' - ')[0])
            design_id = int(design.split(' - ')[0])
        except:
            messagebox.showerror("Error", "Invalid selection!")
            return
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity! Must be a positive integer.")
            return
        
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO worker_production (worker_id, design_id, quantity, date) VALUES (?, ?, ?, ?)",
            (worker_id, design_id, quantity, date)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Production record added successfully!")
        self.load_production_records()
        self.clear_production_form()
    
    def delete_production_record(self):
        selected = self.production_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a record to delete!")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            return
        
        record_id = self.production_tree.item(selected[0])['values'][0]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM worker_production WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Record deleted successfully!")
        self.load_production_records()
        self.clear_production_form()
    
    def clear_production_form(self):
        self.worker_var.set('')
        self.design_var.set('')
        self.quantity_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
    
    def on_production_select(self, event):
        selected = self.production_tree.selection()
        if not selected:
            return
        
        record_data = self.production_tree.item(selected[0])['values']
        self.clear_production_form()
        
        # Set worker
        worker_id = record_data[1]  # Assuming the worker name is in the format "ID - Name"
        workers = get_all_workers()
        for worker in workers:
            if worker[0] == worker_id:
                self.worker_var.set(f"{worker[0]} - {worker[1]}")
                break
        
        # Set design
        design_id = record_data[2]
        designs = get_all_designs()
        for design in designs:
            if design[0] == design_id:
                self.design_var.set(f"{design[0]} - {design[1]}")
                break
        
        # Set quantity and date
        self.quantity_entry.insert(0, record_data[3])
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, record_data[4])

    # ==================== CLIENTS MANAGEMENT ====================
    def show_clients_management(self):
        self.clear_frame()
        
        header = tk.Frame(self.root, bg=self.dark_color)
        header.pack(fill='x')
        tk.Label(header, text="Clients Management", font=('Segoe UI', 18, 'bold'), 
                fg='white', bg=self.dark_color).pack(pady=10)
        
        main_frame = tk.Frame(self.root, bg=self.light_color)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Left Frame - Form
        left_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        left_frame.pack(side='left', fill='y')
        
        tk.Label(left_frame, text="Add/Edit Client", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        form_frame = tk.Frame(left_frame, bg=self.light_color)
        form_frame.pack(pady=10)
        
        labels = ["Name:", "Company:", "Contact:", "Email:", "Address:"]
        self.client_entries = []
        
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg=self.light_color).grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = ttk.Entry(form_frame, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.client_entries.append(entry)
        
        button_frame = tk.Frame(left_frame, bg=self.light_color)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Client", command=self.add_client, 
                 style='Success.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Client", command=self.update_client, 
                 style='Warning.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Client", command=self.delete_client, 
                 style='Danger.TButton').grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_client_form, 
                 style='Primary.TButton').grid(row=0, column=3, padx=5)
        
        # Right Frame - List
        right_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        right_frame.pack(side='right', expand=True, fill='both')
        
        tk.Label(right_frame, text="Clients List", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        # Treeview
        self.clients_tree = ttk.Treeview(right_frame, columns=("ID", "Name", "Company", "Contact", "Email"), 
                                       show='headings', selectmode='browse')
        
        self.clients_tree.heading("ID", text="ID")
        self.clients_tree.heading("Name", text="Name")
        self.clients_tree.heading("Company", text="Company")
        self.clients_tree.heading("Contact", text="Contact")
        self.clients_tree.heading("Email", text="Email")
        
        self.clients_tree.column("ID", width=50, anchor='center')
        self.clients_tree.column("Name", width=150)
        self.clients_tree.column("Company", width=150)
        self.clients_tree.column("Contact", width=120)
        self.clients_tree.column("Email", width=200)
        
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.clients_tree.yview)
        self.clients_tree.configure(yscrollcommand=scrollbar.set)
        
        self.clients_tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.clients_tree.bind('<<TreeviewSelect>>', self.on_client_select)
        
        # Load data
        self.load_clients()
        
        # Home button
        home_btn = ttk.Button(main_frame, text="🏠 Home", command=self.create_main_menu,
                            style='Dark.TButton')
        home_btn.pack(side='bottom', pady=10)
    
    def load_clients(self):
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)
        
        clients = get_all_clients()
        for client in clients:
            self.clients_tree.insert('', 'end', values=client[:5])  # Only show first 5 fields
    
    def add_client(self):
        name = self.client_entries[0].get()
        company = self.client_entries[1].get()
        contact = self.client_entries[2].get()
        email = self.client_entries[3].get()
        address = self.client_entries[4].get()
        
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (name, company, contact, email, address) VALUES (?, ?, ?, ?, ?)",
            (name, company, contact, email, address)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Client added successfully!")
        self.load_clients()
        self.clear_client_form()
    
    def update_client(self):
        selected = self.clients_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a client to update!")
            return
        
        client_id = self.clients_tree.item(selected[0])['values'][0]
        name = self.client_entries[0].get()
        company = self.client_entries[1].get()
        contact = self.client_entries[2].get()
        email = self.client_entries[3].get()
        address = self.client_entries[4].get()
        
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clients SET name=?, company=?, contact=?, email=?, address=? WHERE id=?",
            (name, company, contact, email, address, client_id)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Client updated successfully!")
        self.load_clients()
    
    def delete_client(self):
        selected = self.clients_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a client to delete!")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this client?"):
            return
        
        client_id = self.clients_tree.item(selected[0])['values'][0]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id=?", (client_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Client deleted successfully!")
        self.load_clients()
        self.clear_client_form()
    
    def clear_client_form(self):
        for entry in self.client_entries:
            entry.delete(0, tk.END)
    
    def on_client_select(self, event):
        selected = self.clients_tree.selection()
        if not selected:
            return
        
        client_data = self.clients_tree.item(selected[0])['values']
        self.clear_client_form()
        
        # Check if lengths match before inserting
        for i, value in enumerate(client_data[1:]):  # Skip ID
            self.client_entries[i].insert(0, str(value) if value is not None else "")

    # ==================== ORDERS MANAGEMENT ====================
    def show_orders_management(self):
        self.clear_frame()
        
        header = tk.Frame(self.root, bg=self.dark_color)
        header.pack(fill='x')
        tk.Label(header, text="Orders Management", font=('Segoe UI', 18, 'bold'), 
                fg='white', bg=self.dark_color).pack(pady=10)
        
        main_frame = tk.Frame(self.root, bg=self.light_color)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Left Frame - Form
        left_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        left_frame.pack(side='left', fill='y')
        
        tk.Label(left_frame, text="Add/Edit Order", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        form_frame = tk.Frame(left_frame, bg=self.light_color)
        form_frame.pack(pady=10)
        
        # Client dropdown
        tk.Label(form_frame, text="Client:", bg=self.light_color).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.order_client_var = tk.StringVar()
        self.order_client_dropdown = ttk.Combobox(form_frame, textvariable=self.order_client_var, state='readonly', width=23)
        self.order_client_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        # Design dropdown
        tk.Label(form_frame, text="Design:", bg=self.light_color).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.order_design_var = tk.StringVar()
        self.order_design_dropdown = ttk.Combobox(form_frame, textvariable=self.order_design_var, state='readonly', width=23)
        self.order_design_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        # Quantity
        tk.Label(form_frame, text="Quantity:", bg=self.light_color).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.order_quantity_entry = ttk.Entry(form_frame, width=25)
        self.order_quantity_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Order date
        tk.Label(form_frame, text="Order Date (YYYY-MM-DD):", bg=self.light_color).grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.order_date_entry = ttk.Entry(form_frame, width=25)
        self.order_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.order_date_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Deadline
        tk.Label(form_frame, text="Deadline (YYYY-MM-DD):", bg=self.light_color).grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.order_deadline_entry = ttk.Entry(form_frame, width=25)
        self.order_deadline_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Status
        tk.Label(form_frame, text="Status:", bg=self.light_color).grid(row=5, column=0, sticky='e', padx=5, pady=5)
        self.order_status_var = tk.StringVar(value="Pending")
        status_options = ["Pending", "In Progress", "Completed", "Delivered", "Cancelled"]
        self.order_status_dropdown = ttk.Combobox(form_frame, textvariable=self.order_status_var, 
                                                values=status_options, state='readonly', width=23)
        self.order_status_dropdown.grid(row=5, column=1, padx=5, pady=5)
        
        button_frame = tk.Frame(left_frame, bg=self.light_color)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Order", command=self.add_order, 
                 style='Success.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Order", command=self.update_order, 
                 style='Warning.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Order", command=self.delete_order, 
                 style='Danger.TButton').grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_order_form, 
                 style='Primary.TButton').grid(row=0, column=3, padx=5)
        
        # Right Frame - List
        right_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        right_frame.pack(side='right', expand=True, fill='both')
        
        tk.Label(right_frame, text="Orders List", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        # Treeview
        self.orders_tree = ttk.Treeview(right_frame, columns=("ID", "Client", "Design", "Quantity", "Order Date", "Deadline", "Status"), 
                                      show='headings', selectmode='browse')
        
        self.orders_tree.heading("ID", text="ID")
        self.orders_tree.heading("Client", text="Client")
        self.orders_tree.heading("Design", text="Design")
        self.orders_tree.heading("Quantity", text="Quantity")
        self.orders_tree.heading("Order Date", text="Order Date")
        self.orders_tree.heading("Deadline", text="Deadline")
        self.orders_tree.heading("Status", text="Status")
        
        self.orders_tree.column("ID", width=50, anchor='center')
        self.orders_tree.column("Client", width=150)
        self.orders_tree.column("Design", width=150)
        self.orders_tree.column("Quantity", width=80, anchor='center')
        self.orders_tree.column("Order Date", width=100, anchor='center')
        self.orders_tree.column("Deadline", width=100, anchor='center')
        self.orders_tree.column("Status", width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.orders_tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.orders_tree.bind('<<TreeviewSelect>>', self.on_order_select)
        
        # Load dropdowns and data
        self.load_order_dropdowns()
        self.load_orders()
        
        # Home button
        home_btn = ttk.Button(main_frame, text="🏠 Home", command=self.create_main_menu,
                            style='Dark.TButton')
        home_btn.pack(side='bottom', pady=10)
    
    def load_order_dropdowns(self):
        clients = get_all_clients()
        client_options = [f"{c[0]} - {c[1]}" for c in clients]
        self.order_client_dropdown['values'] = client_options
        
        designs = get_all_designs()
        design_options = [f"{d[0]} - {d[1]}" for d in designs]
        self.order_design_dropdown['values'] = design_options
    
    def load_orders(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        orders = get_all_orders()
        for order in orders:
            self.orders_tree.insert('', 'end', values=order)
    
    def add_order(self):
        client = self.order_client_var.get()
        design = self.order_design_var.get()
        quantity = self.order_quantity_entry.get()
        order_date = self.order_date_entry.get()
        deadline = self.order_deadline_entry.get()
        status = self.order_status_var.get()
        
        if not client or not design:
            messagebox.showerror("Error", "Please select both client and design!")
            return
        
        try:
            client_id = int(client.split(' - ')[0])
            design_id = int(design.split(' - ')[0])
        except:
            messagebox.showerror("Error", "Invalid selection!")
            return
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity! Must be a positive integer.")
            return
        
        try:
            datetime.strptime(order_date, '%Y-%m-%d')
            datetime.strptime(deadline, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (client_id, design_id, quantity, order_date, deadline, status) VALUES (?, ?, ?, ?, ?, ?)",
            (client_id, design_id, quantity, order_date, deadline, status)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Order added successfully!")
        self.load_orders()
        self.clear_order_form()
    
    def update_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an order to update!")
            return
        
        order_id = self.orders_tree.item(selected[0])['values'][0]
        client = self.order_client_var.get()
        design = self.order_design_var.get()
        quantity = self.order_quantity_entry.get()
        order_date = self.order_date_entry.get()
        deadline = self.order_deadline_entry.get()
        status = self.order_status_var.get()
        
        if not client or not design:
            messagebox.showerror("Error", "Please select both client and design!")
            return
        
        try:
            client_id = int(client.split(' - ')[0])
            design_id = int(design.split(' - ')[0])
        except:
            messagebox.showerror("Error", "Invalid selection!")
            return
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity! Must be a positive integer.")
            return
        
        try:
            datetime.strptime(order_date, '%Y-%m-%d')
            datetime.strptime(deadline, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orders SET client_id=?, design_id=?, quantity=?, order_date=?, deadline=?, status=? WHERE id=?",
            (client_id, design_id, quantity, order_date, deadline, status, order_id)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Order updated successfully!")
        self.load_orders()
    
    def delete_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an order to delete!")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this order?"):
            return
        
        order_id = self.orders_tree.item(selected[0])['values'][0]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Order deleted successfully!")
        self.load_orders()
        self.clear_order_form()
    
    def clear_order_form(self):
        self.order_client_var.set('')
        self.order_design_var.set('')
        self.order_quantity_entry.delete(0, tk.END)
        self.order_date_entry.delete(0, tk.END)
        self.order_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.order_deadline_entry.delete(0, tk.END)
        self.order_status_var.set('Pending')
    
    def on_order_select(self, event):
        selected = self.orders_tree.selection()
        if not selected:
            return
        
        order_data = self.orders_tree.item(selected[0])['values']
        self.clear_order_form()
        
        # Set client
        client_id = order_data[1]  # Assuming the client name is in the format "ID - Name"
        clients = get_all_clients()
        for client in clients:
            if client[0] == client_id:
                self.order_client_var.set(f"{client[0]} - {client[1]}")
                break
        
        # Set design
        design_id = order_data[2]
        designs = get_all_designs()
        for design in designs:
            if design[0] == design_id:
                self.order_design_var.set(f"{design[0]} - {design[1]}")
                break
        
        # Set other fields
        self.order_quantity_entry.insert(0, order_data[3])
        self.order_date_entry.delete(0, tk.END)
        self.order_date_entry.insert(0, order_data[4])
        self.order_deadline_entry.insert(0, order_data[5])
        self.order_status_var.set(order_data[6])

    # ==================== INVOICES MANAGEMENT ====================
    def show_invoices_management(self):
        self.clear_frame()
        
        header = tk.Frame(self.root, bg=self.dark_color)
        header.pack(fill='x')
        tk.Label(header, text="Invoices Management", font=('Segoe UI', 18, 'bold'), 
                fg='white', bg=self.dark_color).pack(pady=10)
        
        main_frame = tk.Frame(self.root, bg=self.light_color)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Left Frame - Generate Invoice
        left_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        left_frame.pack(side='left', fill='y')
        
        tk.Label(left_frame, text="Generate Invoice", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        form_frame = tk.Frame(left_frame, bg=self.light_color)
        form_frame.pack(pady=10)
        
        # Order dropdown
        tk.Label(form_frame, text="Order:", bg=self.light_color).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.invoice_order_var = tk.StringVar()
        self.invoice_order_dropdown = ttk.Combobox(form_frame, textvariable=self.invoice_order_var, state='readonly', width=23)
        self.invoice_order_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        # Tax
        tk.Label(form_frame, text="Tax (%):", bg=self.light_color).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.invoice_tax_entry = ttk.Entry(form_frame, width=25)
        self.invoice_tax_entry.insert(0, "0")
        self.invoice_tax_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Discount
        tk.Label(form_frame, text="Discount:", bg=self.light_color).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.invoice_discount_entry = ttk.Entry(form_frame, width=25)
        self.invoice_discount_entry.insert(0, "0")
        self.invoice_discount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        button_frame = tk.Frame(left_frame, bg=self.light_color)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Generate Invoice", command=self.generate_invoice, 
                 style='Success.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Print Invoice", command=self.print_invoice, 
                 style='Primary.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_invoice_form, 
                 style='Primary.TButton').grid(row=0, column=2, padx=5)
        
        # Right Frame - Invoices List
        right_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        right_frame.pack(side='right', expand=True, fill='both')
        
        tk.Label(right_frame, text="Invoices List", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        # Treeview
        self.invoices_tree = ttk.Treeview(right_frame, columns=("ID", "Order ID", "Client", "Date", "Amount", "Status"), 
                                        show='headings', selectmode='browse')
        
        self.invoices_tree.heading("ID", text="ID")
        self.invoices_tree.heading("Order ID", text="Order ID")
        self.invoices_tree.heading("Client", text="Client")
        self.invoices_tree.heading("Date", text="Date")
        self.invoices_tree.heading("Amount", text="Amount")
        self.invoices_tree.heading("Status", text="Status")
        
        self.invoices_tree.column("ID", width=50, anchor='center')
        self.invoices_tree.column("Order ID", width=80, anchor='center')
        self.invoices_tree.column("Client", width=150)
        self.invoices_tree.column("Date", width=100, anchor='center')
        self.invoices_tree.column("Amount", width=100, anchor='e')
        self.invoices_tree.column("Status", width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.invoices_tree.yview)
        self.invoices_tree.configure(yscrollcommand=scrollbar.set)
        
        self.invoices_tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.invoices_tree.bind('<<TreeviewSelect>>', self.on_invoice_select)
        
        # Load dropdown and data
        self.load_invoice_dropdown()
        self.load_invoices()
        
        # Home button
        home_btn = ttk.Button(main_frame, text="🏠 Home", command=self.create_main_menu,
                            style='Dark.TButton')
        home_btn.pack(side='bottom', pady=10)
    
    def load_invoice_dropdown(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT o.id, c.name, d.name 
        FROM orders o
        JOIN clients c ON o.client_id = c.id
        JOIN designs d ON o.design_id = d.id
        WHERE o.status != 'Cancelled' AND o.id NOT IN (SELECT order_id FROM invoices)
        ''')
        
        orders = cursor.fetchall()
        conn.close()
        
        order_options = [f"{o[0]} - {o[1]} ({o[2]})" for o in orders]
        self.invoice_order_dropdown['values'] = order_options
    
    def load_invoices(self):
        for item in self.invoices_tree.get_children():
            self.invoices_tree.delete(item)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT i.id, i.order_id, c.name, i.invoice_date, i.total_amount, i.status
        FROM invoices i
        JOIN orders o ON i.order_id = o.id
        JOIN clients c ON o.client_id = c.id
        ORDER BY i.invoice_date DESC
        ''')
        
        invoices = cursor.fetchall()
        conn.close()
        
        for invoice in invoices:
            self.invoices_tree.insert('', 'end', values=invoice)
    
    def generate_invoice(self):
        order = self.invoice_order_var.get()
        tax = self.invoice_tax_entry.get()
        discount = self.invoice_discount_entry.get()
        
        if not order:
            messagebox.showerror("Error", "Please select an order!")
            return
        
        try:
            order_id = int(order.split(' - ')[0])
        except:
            messagebox.showerror("Error", "Invalid order selection!")
            return
        
        try:
            tax = float(tax) if tax else 0
            discount = float(discount) if discount else 0
        except ValueError:
            messagebox.showerror("Error", "Invalid tax or discount value!")
            return
        
        invoice_data = create_invoice(order_id, tax, discount)
        if invoice_data:
            messagebox.showinfo("Success", f"Invoice #{invoice_data['invoice_id']} generated successfully!")
            self.load_invoice_dropdown()
            self.load_invoices()
            self.clear_invoice_form()
    
    def print_invoice(self):
            selected = self.invoices_tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select an invoice to print!")
                return
            
            invoice_id = self.invoices_tree.item(selected[0])['values'][0]
            
            # Get invoice details
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
            SELECT i.id, i.order_id, c.name, c.company, c.address, 
                d.name, d.base_price, o.quantity, 
                i.invoice_date, i.amount, i.tax, i.discount, i.total_amount
            FROM invoices i
            JOIN orders o ON i.order_id = o.id
            JOIN clients c ON o.client_id = c.id
            JOIN designs d ON o.design_id = d.id
            WHERE i.id = ?
            ''', (invoice_id,))
            
            invoice = cursor.fetchone()
            conn.close()
            
            if not invoice:
                messagebox.showerror("Error", "Invoice not found!")
                return
            
            # Prepare data for template
            invoice_data = {
                'invoice_id': invoice[0],
                'order_id': invoice[1],
                'client_name': invoice[2],
                'client_company': invoice[3],
                'client_address': invoice[4],
                'design_name': invoice[5],
                'unit_price': invoice[6],
                'quantity': invoice[7],
                'invoice_date': invoice[8],
                'subtotal': invoice[9],
                'tax': invoice[10],
                'discount': invoice[11],
                'total': invoice[12]
            }
            
            # Load HTML template
            template_path = os.path.join('invoice_template', 'template.html')
            try:
                with open(template_path, 'r') as f:
                    template_content = f.read()
                
                # Create template and render with data
                template = Template(template_content)
                html_content = template.render(**invoice_data)
                
                # Save to temporary file
                temp_file = os.path.join('invoice_template', f'invoice_{invoice_id}.html')
                with open(temp_file, 'w') as f:
                    f.write(html_content)
                
                # Open in browser
                webbrowser.open('file://' + os.path.abspath(temp_file))
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate invoice: {str(e)}")


    def clear_invoice_form(self):
        self.invoice_order_var.set('')
        self.invoice_tax_entry.delete(0, tk.END)
        self.invoice_tax_entry.insert(0, "0")
        self.invoice_discount_entry.delete(0, tk.END)
        self.invoice_discount_entry.insert(0, "0")
    
    def on_invoice_select(self, event):
        selected = self.invoices_tree.selection()
        if not selected:
            return
        
        invoice_data = self.invoices_tree.item(selected[0])['values']
        # You can implement details display if needed

    # ==================== SALARY REPORTS ====================
    def show_salary_reports(self):
        self.clear_frame()
        
        header = tk.Frame(self.root, bg=self.dark_color)
        header.pack(fill='x')
        tk.Label(header, text="Salary Reports", font=('Segoe UI', 18, 'bold'), 
                fg='white', bg=self.dark_color).pack(pady=10)
        
        main_frame = tk.Frame(self.root, bg=self.light_color)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Left Frame - Filters
        left_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        left_frame.pack(side='left', fill='y')
        
        tk.Label(left_frame, text="Generate Salary Report", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        form_frame = tk.Frame(left_frame, bg=self.light_color)
        form_frame.pack(pady=10)
        
        # Worker dropdown
        tk.Label(form_frame, text="Worker:", bg=self.light_color).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.salary_worker_var = tk.StringVar()
        self.salary_worker_dropdown = ttk.Combobox(form_frame, textvariable=self.salary_worker_var, state='readonly', width=23)
        self.salary_worker_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        # Month dropdown
        tk.Label(form_frame, text="Month:", bg=self.light_color).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.salary_month_var = tk.StringVar()
        self.salary_month_dropdown = ttk.Combobox(form_frame, textvariable=self.salary_month_var, 
                                                values=list(range(1, 13)), state='readonly', width=23)
        self.salary_month_dropdown.set(datetime.now().month)
        self.salary_month_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        # Year dropdown
        tk.Label(form_frame, text="Year:", bg=self.light_color).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.salary_year_var = tk.StringVar()
        self.salary_year_dropdown = ttk.Combobox(form_frame, textvariable=self.salary_year_var, 
                                               values=list(range(2020, datetime.now().year + 1)), 
                                               state='readonly', width=23)
        self.salary_year_dropdown.set(datetime.now().year)
        self.salary_year_dropdown.grid(row=2, column=1, padx=5, pady=5)
        
        button_frame = tk.Frame(left_frame, bg=self.light_color)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Generate Report", command=self.generate_salary_report, 
                 style='Success.TButton').grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Print Report", command=self.print_salary_report, 
                 style='Primary.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_salary_form, 
                 style='Primary.TButton').grid(row=0, column=2, padx=5)
        
        # Right Frame - Report
        right_frame = tk.Frame(main_frame, bg=self.light_color, padx=10, pady=10)
        right_frame.pack(side='right', expand=True, fill='both')
        
        tk.Label(right_frame, text="Salary Report", font=('Segoe UI', 12, 'bold'), 
                bg=self.light_color).pack(pady=5)
        
        # Report text
        self.report_text = tk.Text(right_frame, wrap=tk.WORD, font=('Segoe UI', 10), height=20)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar.set)
        
        self.report_text.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')
        
        # Load dropdown
        self.load_salary_dropdown()
        
        # Home button
        home_btn = ttk.Button(main_frame, text="🏠 Home", command=self.create_main_menu,
                            style='Dark.TButton')
        home_btn.pack(side='bottom', pady=10)
    
    def load_salary_dropdown(self):
        workers = get_all_workers()
        worker_options = [f"{w[0]} - {w[1]}" for w in workers]
        self.salary_worker_dropdown['values'] = worker_options
    
    def generate_salary_report(self):
        worker = self.salary_worker_var.get()
        month = self.salary_month_var.get()
        year = self.salary_year_var.get()
        
        if not worker or not month or not year:
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        try:
            worker_id = int(worker.split(' - ')[0])
            month = int(month)
            year = int(year)
        except:
            messagebox.showerror("Error", "Invalid selection!")
            return
        
        salary_data = calculate_worker_salary(worker_id, month, year)
        
        # Generate report text
        report = f"Salary Report\n{'='*40}\n"
        report += f"Worker: {worker}\n"
        report += f"Period: {month}/{year}\n"
        report += f"{'-'*40}\n"
        report += f"Total Items Produced: {salary_data['total_quantity']}\n"
        report += f"Hours Worked: {salary_data['hours_worked']:.2f}\n"
        report += f"Hourly Rate: ${salary_data['hourly_rate']:.2f}\n"
        report += f"{'-'*40}\n"
        report += f"Total Salary: ${salary_data['salary']:.2f}\n"
        report += f"{'='*40}"
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report)
    
    def print_salary_report(self):
        report_text = self.report_text.get(1.0, tk.END)
        if not report_text.strip():
            messagebox.showerror("Error", "No report to print!")
            return
        
        # Save to temporary file
        temp_file = os.path.join('invoice_template', 'salary_report.txt')
        with open(temp_file, 'w') as f:
            f.write(report_text)
        
        # Open in default text editor
        webbrowser.open('file://' + os.path.abspath(temp_file))
    
    def clear_salary_form(self):
        self.salary_worker_var.set('')
        self.salary_month_var.set(datetime.now().month)
        self.salary_year_var.set(datetime.now().year)
        self.report_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FactoryManagementGUI(root)
    root.mainloop()