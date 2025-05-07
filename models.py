from datetime import datetime

class Worker:
    def __init__(self, name, contact=None, joining_date=None, hourly_rate=0):
        self.name = name
        self.contact = contact
        self.joining_date = joining_date or datetime.now().strftime('%Y-%m-%d')
        self.hourly_rate = hourly_rate

    @classmethod
    def from_db_row(cls, row):
        return cls(
            name=row[1],
            contact=row[2],
            joining_date=row[3],
            hourly_rate=row[4]
        )

class Design:
    def __init__(self, name, description=None, base_price=0, complexity_level=1):
        self.name = name
        self.description = description
        self.base_price = base_price
        self.complexity_level = complexity_level

    @classmethod
    def from_db_row(cls, row):
        return cls(
            name=row[1],
            description=row[2],
            base_price=row[3],
            complexity_level=row[4]
        )

class Client:
    def __init__(self, name, company=None, contact=None, email=None, address=None):
        self.name = name
        self.company = company
        self.contact = contact
        self.email = email
        self.address = address

    @classmethod
    def from_db_row(cls, row):
        return cls(
            name=row[1],
            company=row[2],
            contact=row[3],
            email=row[4],
            address=row[5]
        )

class Order:
    def __init__(self, client_id, design_id, quantity, deadline, order_date=None, status='Pending'):
        self.client_id = client_id
        self.design_id = design_id
        self.quantity = quantity
        self.order_date = order_date or datetime.now().strftime('%Y-%m-%d')
        self.deadline = deadline
        self.status = status

    @classmethod
    def from_db_row(cls, row):
        return cls(
            client_id=row[1],
            design_id=row[2],
            quantity=row[3],
            deadline=row[5],
            order_date=row[4],
            status=row[6]
        )

class ProductionRecord:
    def __init__(self, worker_id, design_id, quantity, date=None):
        self.worker_id = worker_id
        self.design_id = design_id
        self.quantity = quantity
        self.date = date or datetime.now().strftime('%Y-%m-%d')

    @classmethod
    def from_db_row(cls, row):
        return cls(
            worker_id=row[1],
            design_id=row[2],
            quantity=row[3],
            date=row[4]
        )