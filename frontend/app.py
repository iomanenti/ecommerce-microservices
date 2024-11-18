from flask import Flask, render_template, request, redirect, url_for, flash
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
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        data = {"username": username, "email": email, "password": password}
        
        response = requests.post(f"{USER_SERVICE_URL}/register", json=data)
        if response.status_code == 201:
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        else:
            flash(response.json().get('error', 'Registration failed'), 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = {"username": username, "password": password}
        
        response = requests.post(f"{USER_SERVICE_URL}/login", json=data)
        if response.status_code == 200:
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('account', username=username))
        else:
            flash(response.json().get('error', 'Login failed'), 'danger')
    
    return render_template('login.html')

@app.route('/account/<username>', methods=['GET', 'POST'])
def account(username):
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
    response = requests.delete(f"{USER_SERVICE_URL}/delete-account/{username}")
    if response.status_code == 200:
        flash('Account deleted successfully!', 'success')
        return redirect(url_for('home'))
    else:
        flash(response.json().get('error', 'Delete failed'), 'danger')
    
    return redirect(url_for('account', username=username))

@app.route('/products')
def products():
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
    products = response.json() if response.status_code == 200 else []
    return render_template('products.html', products=products)

@app.route('/cart/<user_id>')
def cart(user_id):
    response = requests.get(f"{CART_SERVICE_URL}/cart/{user_id}")
    cart_items = response.json().get('items', [])
    return render_template('cart.html', cart_items=cart_items, user_id=user_id)

@app.route('/add-to-cart/<user_id>/<product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    data = {"product_id": product_id, "quantity": 1}
    requests.post(f"{CART_SERVICE_URL}/cart/{user_id}", json=data)
    return redirect(url_for('cart', user_id=user_id))

@app.route('/place-order/<user_id>', methods=['POST'])
def place_order(user_id):
    cart_response = requests.get(f"{CART_SERVICE_URL}/cart/{user_id}")
    cart_items = cart_response.json().get('items', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    order_data = {"user_id": user_id, "items": cart_items, "total_price": total_price}
    requests.post(f"{ORDER_SERVICE_URL}/order", json=order_data)
    return redirect(url_for('cart', user_id=user_id))

if __name__ == '__main__':
    app.run(port=5000, debug=True)