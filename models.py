import json

import json

class User:
    def __init__(self, username, email, hashed_password):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "hashed_password": self.hashed_password
        }

def load_users():
    """Load users from the JSON file."""
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_users(users):
    """Save users to the JSON file."""
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)


class Product:
    def __init__(self, product_id, name, description, price, stock):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock
        }

def load_products():
    try:
        with open('products.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_products(products):
    with open('products.json', 'w') as file:
        json.dump(products, file, indent=4)

class Cart:
    def __init__(self, user_id, items):
        self.user_id = user_id
        self.items = items

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "items": self.items
        }

def load_carts():
    try:
        with open('carts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_carts(carts):
    with open('carts.json', 'w') as file:
        json.dump(carts, file, indent=4)


class Order:
    def __init__(self, order_id, user_id, items, total_price):
        self.order_id = order_id
        self.user_id = user_id
        self.items = items
        self.total_price = total_price

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "items": self.items,
            "total_price": self.total_price
        }

def load_orders():
    try:
        with open('orders.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_orders(orders):
    with open('orders.json', 'w') as file:
        json.dump(orders, file, indent=4)
