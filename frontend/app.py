from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Microservice URLs
USER_SERVICE_URL = "http://localhost:5001"
PRODUCT_SERVICE_URL = "http://localhost:5002"
CART_SERVICE_URL = "http://localhost:5003"
ORDER_SERVICE_URL = "http://localhost:5004"

@app.route('/')
def home():
    """Render the home page."""
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_admin = 'is_admin' in request.form  # Checkbox is present if checked
        
        data = {
            "username": username,
            "email": email,
            "password": password,
            "is_admin": is_admin
        }
        
        response = requests.post(f"{USER_SERVICE_URL}/register", json=data)
        if response.status_code == 201:
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        else:
            flash(response.json().get('error', 'Registration failed'), 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = {"username": username, "password": password}
        
        response = requests.post(f"{USER_SERVICE_URL}/login", json=data)
        if response.status_code == 200:
            user_data = response.json()
            session['username'] = username  # Store username in the session
            session['is_admin'] = user_data['is_admin']  # Store admin status
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('products'))
        else:
            flash(response.json().get('error', 'Login failed'), 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()  # Clear all session data
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

@app.route('/account/<username>', methods=['GET', 'POST'])
def account(username):
    """Handle account updates."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        data = {}
        if email:
            data['email'] = email
        if password:
            data['password'] = password
        
        response = requests.put(f"{USER_SERVICE_URL}/update-account/{username}", json=data)
        if response.status_code == 200:
            flash('Account updated successfully!', 'success')
        else:
            flash(response.json().get('error', 'Update failed'), 'danger')
    
    return render_template('account.html', username=username)

@app.route('/delete-account/<username>', methods=['POST'])
def delete_account(username):
    """Handle account deletion."""
    response = requests.delete(f"{USER_SERVICE_URL}/delete-account/{username}")
    if response.status_code == 200:
        flash('Account deleted successfully!', 'success')
        return redirect(url_for('home'))
    else:
        flash(response.json().get('error', 'Delete failed'), 'danger')
    
    return redirect(url_for('account', username=username))

@app.route('/cart/<string:user_id>', methods=['GET'])
def cart(user_id):
    """View the cart for the logged-in user."""
    response = requests.get(f"{CART_SERVICE_URL}/cart/{user_id}")
    cart = response.json()
    cart_items = cart.get('items', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, user_id=user_id)

@app.route('/add-to-cart/<string:user_id>/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    """Add a product to the user's cart."""
    data = {
        "product_id": product_id,
        "name": request.form['name'],
        "price": float(request.form['price']),
        "quantity": int(request.form['quantity'])
    }
    requests.post(f"{CART_SERVICE_URL}/cart/{user_id}", json=data)
    flash(f"Added {data['name']} to your cart.", "success")
    return redirect(url_for('products'))

@app.route('/cart/<string:user_id>/product/<int:product_id>', methods=['POST'])
def delete_from_cart(user_id, product_id):
    """Remove a specific product from the cart."""
    requests.delete(f"{CART_SERVICE_URL}/cart/{user_id}/product/{product_id}")
    flash("Product removed from cart.", "success")
    return redirect(url_for('cart', user_id=user_id))

@app.route('/place-order/<string:user_id>', methods=['POST'])
def place_order(user_id):
    """Place an order and clear the cart."""
    cart_response = requests.get(f"{CART_SERVICE_URL}/cart/{user_id}")
    cart = cart_response.json()
    cart_items = cart.get('items', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    # Place the order
    order_data = {"user_id": user_id, "items": cart_items, "total_price": total_price}
    requests.post(f"{ORDER_SERVICE_URL}/order", json=order_data)

    flash("Order placed successfully! Your cart has been saved as an order.", "success")
    return redirect(url_for('cart', user_id=user_id))

@app.route('/products', methods=['GET', 'POST'])
def products():
    """Display all products."""
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
    products = response.json() if response.status_code == 200 else []
    is_admin = session.get('is_admin', False)  # Retrieve is_admin value from the session
    return render_template('products.html', products=products, is_admin=is_admin)

@app.route('/add-product', methods=['POST'])
def add_product():
    """Add a new product (Admin only)."""
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "price": float(request.form['price']),
        "stock": int(request.form['stock'])
    }
    requests.post(f"{PRODUCT_SERVICE_URL}/products", json=data)
    return redirect(url_for('products'))

@app.route('/products/<int:product_id>/edit', methods=['POST'])
def edit_product(product_id):
    """Edit a product's details (Admin only)."""
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "price": float(request.form['price']),
        "stock": int(request.form['stock'])
    }
    response = requests.put(f"{PRODUCT_SERVICE_URL}/products/{product_id}", json=data)
    if response.status_code == 200:
        flash("Product updated successfully.", "success")
    else:
        flash(response.json().get('error', 'Failed to update product'), "danger")
    return redirect(url_for('products'))

@app.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    """Delete a product (Admin only)."""
    response = requests.delete(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
    if response.status_code == 200:
        flash("Product deleted successfully.", "success")
    else:
        flash(response.json().get('error', 'Failed to delete product'), "danger")
    return redirect(url_for('products'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)