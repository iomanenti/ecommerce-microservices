from flask import Flask, request, jsonify
from models import Order, load_orders, save_orders

app = Flask(__name__)

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    orders = load_orders()
    new_order = Order(len(orders) + 1, data['user_id'], data['items'], data['total_price'])
    orders.append(new_order.to_dict())
    save_orders(orders)
    return jsonify({"message": "Order placed successfully"}), 201

if __name__ == "__main__":
    app.run(port=5004, debug=True)