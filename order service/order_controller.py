from flask import Flask, request, jsonify
from models import Order, load_orders, save_orders
import requests

app = Flask(__name__)

@app.route('/order', methods=['POST'])
def place_order():
    """Place an order."""
    data = request.json
    orders = load_orders()

    new_order = Order(
        order_id=len(orders) + 1,
        user_id=data['user_id'],
        items=data['items'],
        total_price=data['total_price']
    ).to_dict()

    # Save the order
    orders.append(new_order)
    save_orders(orders)

    # Clear the cart and stack it as an ordered cart
    requests.delete(f"http://localhost:5003/cart/{data['user_id']}")

    return jsonify({"message": "Order placed successfully", "order": new_order}), 201


if __name__ == '__main__':
    app.run(port=5004, debug=True)
