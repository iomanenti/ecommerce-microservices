from flask import Flask, request, jsonify, json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.models import Cart, load_carts, save_carts

app = Flask(__name__)

@app.route('/cart/<string:user_id>', methods=['GET'])
def get_cart(user_id):
    """Get the cart for a specific user."""
    carts = load_carts()
    cart = next((c for c in carts if c['user_id'] == user_id), None)
    if not cart:
        return jsonify({"items": []}), 200
    return jsonify(cart), 200

@app.route('/cart/<string:user_id>', methods=['POST'])
def add_to_cart(user_id):
    """Add a product to the user's active cart."""
    data = request.json
    carts = load_carts()
    cart = next((c for c in carts if c['user_id'] == user_id and c.get('status') == 'active'), None)

    if not cart:
        # Create a new active cart if it doesn't exist
        cart = {
            "user_id": user_id,
            "items": [],
            "status": "active"
        }
        carts.append(cart)

    # Check if the product already exists in the cart
    existing_item = next((item for item in cart['items'] if item['product_id'] == data['product_id']), None)
    if existing_item:
        existing_item['quantity'] += data['quantity']
    else:
        cart['items'].append(data)

    save_carts(carts)
    return jsonify({"message": "Item added to cart"}), 201

@app.route('/cart/<string:user_id>', methods=['DELETE'])
def clear_cart(user_id):
    """Clear the user's cart after saving it to the ordered carts."""
    carts = load_carts()
    cart = next((c for c in carts if c['user_id'] == user_id), None)

    if cart:
        # Save the cart with a "status" field
        cart['status'] = 'ordered'
        save_ordered_cart(cart)

        # Remove the cart from active carts
        carts = [c for c in carts if c['user_id'] != user_id]
        save_carts(carts)

    return jsonify({"message": "Cart cleared and saved to orders"}), 200

@app.route('/cart/<string:user_id>/product/<int:product_id>', methods=['DELETE'])
def delete_product_from_cart(user_id, product_id):
    """Delete a single product from the user's cart."""
    carts = load_carts()
    cart = next((c for c in carts if c['user_id'] == user_id and c.get('status') == 'active'), None)

    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    # Filter out the product to be deleted
    cart['items'] = [item for item in cart['items'] if item['product_id'] != product_id]
    save_carts(carts)

    return jsonify({"message": "Product removed from cart"}), 200

def save_ordered_cart(cart):
    """Append the ordered cart to the ordered carts file."""
    try:
        with open('cart-service/carts.json', 'r') as file:
            carts = json.load(file)
    except FileNotFoundError:
        carts = []

    carts.append(cart)

    with open('cart-service/carts.json', 'w') as file:
        json.dump(carts, file, indent=4)

if __name__ == '__main__':
    app.run(port=5003, debug=True)