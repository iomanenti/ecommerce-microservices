from flask import Flask, request, jsonify
from models import Product, load_products, save_products

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(load_products()), 200

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    products = load_products()
    new_product = Product(len(products) + 1, data['name'], data['description'], data['price'], data['stock'])
    products.append(new_product.to_dict())
    save_products(products)
    return jsonify({"message": "Product added successfully"}), 201

if __name__ == "__main__":
    app.run(port=5002, debug=True)
