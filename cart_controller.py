from flask import Flask, request, jsonify
from models import Cart, load_carts, save_carts

app = Flask(__name__)

@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    carts = load_carts()
    user_cart = next((cart for cart in carts if cart['user_id'] == user_id), None)
    return jsonify(user_cart if user_cart else {"items": []}), 200

@app.route('/cart/<user_id>', methods=['POST'])
def add_to_cart(user_id):
    data = request.json
    carts = load_carts()
    user_cart = next((cart for cart in carts if cart['user_id'] == user_id), None)
    if user_cart:
        user_cart['items'].append(data)
    else:
        new_cart = Cart(user_id, [data])
        carts.append(new_cart.to_dict())
    save_carts(carts)
    return jsonify({"message": "Item added to cart"}), 201

if __name__ == "__main__":
    app.run(port=5003, debug=True)
