from flask import Flask, request, jsonify, json
from models import Cart, load_carts, save_carts

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
    """Add a product to the user's cart."""
    data = request.json
    carts = load_carts()
    cart = next((c for c in carts if c['user_id'] == user_id), None)

    if not cart:
        cart = Cart(user_id, []).to_dict()
        carts.append(cart)

    # Check if product is already in the cart
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

def save_ordered_cart(cart):
    """Append the ordered cart to the ordered carts file."""
    try:
        with open('carts.json', 'r') as file:
            carts = json.load(file)
    except FileNotFoundError:
        carts = []

    carts.append(cart)

    with open('carts.json', 'w') as file:
        json.dump(carts, file, indent=4)

if __name__ == '__main__':
    app.run(port=5003, debug=True)