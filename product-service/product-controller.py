from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.models import Product, load_products, save_products

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def list_products():
    """List all products."""
    return jsonify(load_products()), 200

@app.route('/products', methods=['POST'])
def add_product():
    """Add a new product."""
    data = request.json
    products = load_products()

    # Create a new product instance
    new_product = Product(len(products) + 1, data['name'], data['description'], data['price'], data['stock'])
    
    # Append the new product to the list and save
    products.append(new_product.to_dict())
    save_products(products)
    
    return jsonify({"message": "Product added successfully"}), 201

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product by its ID (Admin only)."""
    products = load_products()
    
    # Filter out the product to be deleted
    updated_products = [p for p in products if p['product_id'] != product_id]

    # Check if the product was found and deleted
    if len(updated_products) == len(products):
        return jsonify({"error": "Product not found"}), 404

    save_products(updated_products)
    return jsonify({"message": "Product deleted successfully"}), 200

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product's details (Admin only)."""
    data = request.json
    products = load_products()
    
    # Find the product by ID
    product = next((p for p in products if p['product_id'] == product_id), None)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Update the product fields with provided data
    product['name'] = data.get('name', product['name'])
    product['description'] = data.get('description', product['description'])
    product['price'] = data.get('price', product['price'])
    product['stock'] = data.get('stock', product['stock'])

    save_products(products)
    return jsonify({"message": "Product updated successfully"}), 200

if __name__ == "__main__":
    app.run(port=5002, debug=True)