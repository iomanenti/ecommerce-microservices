import json

# User class to represent a user in the system
class User:
    def __init__(self, username, email, hashed_password):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

    def to_dict(self):
        """Convert User object to dictionary."""
        return {
            "username": self.username,
            "email": self.email,
            "hashed_password": self.hashed_password
        }

# Function to load users from a JSON file
def load_users():
    """Load users from the JSON file."""
    try:
        with open('user-service/users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save users to a JSON file
def save_users(users):
    """Save users to the JSON file."""
    with open('user-service/users.json', 'w') as file:
        json.dump(users, file, indent=4)

# Product class to represent a product in the system
class Product:
    def __init__(self, product_id, name, description, price, stock):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    def to_dict(self):
        """Convert Product object to dictionary."""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock
        }

# Function to load products from a JSON file
def load_products():
    """Load all products from the JSON file."""
    try:
        with open('product-service/products.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save products to a JSON file
def save_products(products):
    """Save all products back to the JSON file."""
    with open('product-service/products.json', 'w') as file:
        json.dump(products, file, indent=4)

# Cart class to represent a shopping cart in the system
class Cart:
    def __init__(self, user_id, items):
        self.user_id = user_id
        self.items = items

    def to_dict(self):
        """Convert Cart object to dictionary."""
        return {
            "user_id": self.user_id,
            "items": self.items
        }

# Function to load carts from a JSON file
def load_carts():
    """Load all carts from the JSON file."""
    try:
        with open('cart-service/carts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save carts to a JSON file
def save_carts(carts):
    """Save all carts back to the JSON file."""
    with open('cart-service/carts.json', 'w') as file:
        json.dump(carts, file, indent=4)

# Order class to represent an order in the system
class Order:
    def __init__(self, order_id, user_id, items, total_price):
        self.order_id = order_id
        self.user_id = user_id
        self.items = items
        self.total_price = total_price

    def to_dict(self):
        """Convert Order object to dictionary."""
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "items": self.items,
            "total_price": self.total_price
        }

# Function to load orders from a JSON file
def load_orders():
    """Load orders from the JSON file."""
    try:
        with open('order-service/orders.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save orders to a JSON file
def save_orders(orders):
    """Save orders to the JSON file."""
    with open('order-service/orders.json', 'w') as file:
        json.dump(orders, file, indent=4)