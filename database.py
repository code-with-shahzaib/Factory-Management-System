import sqlite3
from datetime import datetime

def initialize_database():
    conn = sqlite3.connect('factory.db')
    cursor = conn.cursor()
    
    # Workers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS workers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT,
        joining_date TEXT,
        hourly_rate REAL DEFAULT 0
    )
    ''')
    
    # Designs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS designs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        base_price REAL DEFAULT 0,
        complexity_level INTEGER DEFAULT 1
    )
    ''')
    
    # Worker Production table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS worker_production (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER,
        design_id INTEGER,
        quantity INTEGER,
        date TEXT,
        FOREIGN KEY(worker_id) REFERENCES workers(id),
        FOREIGN KEY(design_id) REFERENCES designs(id)
    )
    ''')
    
    # Clients table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        company TEXT,
        contact TEXT,
        email TEXT,
        address TEXT
    )
    ''')
    
    # Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        design_id INTEGER,
        quantity INTEGER,
        order_date TEXT,
        deadline TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY(client_id) REFERENCES clients(id),
        FOREIGN KEY(design_id) REFERENCES designs(id)
    )
    ''')
    
    # Invoices table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        invoice_date TEXT,
        amount REAL,
        tax REAL DEFAULT 0,
        discount REAL DEFAULT 0,
        total_amount REAL,
        status TEXT DEFAULT 'Unpaid',
        FOREIGN KEY(order_id) REFERENCES orders(id)
    )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('factory.db')

# Helper functions for all modules
def get_all_workers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workers ORDER BY name")
    workers = cursor.fetchall()
    conn.close()
    return workers

def get_all_designs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM designs ORDER BY name")
    designs = cursor.fetchall()
    conn.close()
    return designs

def get_all_clients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients ORDER BY name")
    clients = cursor.fetchall()
    conn.close()
    return clients

def get_all_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT o.id, c.name, d.name, o.quantity, o.order_date, o.deadline, o.status 
    FROM orders o
    JOIN clients c ON o.client_id = c.id
    JOIN designs d ON o.design_id = d.id
    ORDER BY o.order_date DESC
    ''')
    orders = cursor.fetchall()
    conn.close()
    return orders

def get_production_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT wp.id, w.name, d.name, wp.quantity, wp.date 
    FROM worker_production wp
    JOIN workers w ON wp.worker_id = w.id
    JOIN designs d ON wp.design_id = d.id
    ORDER BY wp.date DESC
    ''')
    records = cursor.fetchall()
    conn.close()
    return records

def calculate_worker_salary(worker_id, month, year):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get hourly rate
    cursor.execute("SELECT hourly_rate FROM workers WHERE id = ?", (worker_id,))
    hourly_rate = cursor.fetchone()[0]
    
    # Get production records for the month
    cursor.execute('''
    SELECT SUM(quantity) as total_quantity
    FROM worker_production
    WHERE worker_id = ? AND strftime('%Y-%m', date) = ?
    ''', (worker_id, f"{year}-{month:02d}"))
    
    total_quantity = cursor.fetchone()[0] or 0
    conn.close()
    
    # Simple calculation: Assume 1 item takes 0.1 hour to produce
    hours_worked = total_quantity * 0.1
    salary = hours_worked * hourly_rate
    
    return {
        'worker_id': worker_id,
        'month': month,
        'year': year,
        'total_quantity': total_quantity,
        'hours_worked': hours_worked,
        'hourly_rate': hourly_rate,
        'salary': salary
    }

def create_invoice(order_id, tax=0, discount=0):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get order details
    cursor.execute('''
    SELECT o.id, c.name, c.company, c.address, d.name, d.base_price, o.quantity, o.order_date
    FROM orders o
    JOIN clients c ON o.client_id = c.id
    JOIN designs d ON o.design_id = d.id
    WHERE o.id = ?
    ''', (order_id,))
    
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return None
    
    # Calculate amounts
    subtotal = order[5] * order[6]
    total = subtotal + (subtotal * tax / 100) - discount
    
    # Insert invoice
    invoice_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
    INSERT INTO invoices (order_id, invoice_date, amount, tax, discount, total_amount, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (order_id, invoice_date, subtotal, tax, discount, total, 'Unpaid'))
    
    invoice_id = cursor.lastrowid
    
    # Update order status
    cursor.execute("UPDATE orders SET status = 'Invoiced' WHERE id = ?", (order_id,))
    
    conn.commit()
    conn.close()
    
    return {
        'invoice_id': invoice_id,
        'order_id': order_id,
        'client_name': order[1],
        'client_company': order[2],
        'client_address': order[3],
        'design_name': order[4],
        'unit_price': order[5],
        'quantity': order[6],
        'order_date': order[7],
        'invoice_date': invoice_date,
        'subtotal': subtotal,
        'tax': tax,
        'discount': discount,
        'total': total
    }