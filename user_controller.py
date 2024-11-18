from flask import Flask, request, jsonify
import bcrypt
from models import User, load_users, save_users

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    """Register a new user."""
    data = request.json
    users = load_users()

    if any(user['username'] == data['username'] for user in users):
        return jsonify({"error": "Username already exists"}), 400

    if any(user['email'] == data['email'] for user in users):
        return jsonify({"error": "Email already exists"}), 400

    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(data['username'], data['email'], hashed_pw)
    users.append(new_user.to_dict())
    save_users(users)

    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login_user():
    """Log in an existing user."""
    data = request.json
    users = load_users()

    user = next((u for u in users if u['username'] == data['username']), None)
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['hashed_password'].encode('utf-8')):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": f"Welcome, {user['username']}!"}), 200


@app.route('/update-account/<username>', methods=['PUT'])
def update_account(username):
    """Update account information."""
    data = request.json
    users = load_users()

    user = next((u for u in users if u['username'] == username), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if 'email' in data:
        if any(u['email'] == data['email'] and u['username'] != username for u in users):
            return jsonify({"error": "Email already in use"}), 400
        user['email'] = data['email']

    if 'password' in data:
        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user['hashed_password'] = hashed_pw

    save_users(users)
    return jsonify({"message": "Account updated successfully"}), 200


@app.route('/delete-account/<username>', methods=['DELETE'])
def delete_account(username):
    """Delete an account."""
    users = load_users()

    user = next((u for u in users if u['username'] == username), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    users = [u for u in users if u['username'] != username]
    save_users(users)
    return jsonify({"message": "Account deleted successfully"}), 200


if __name__ == '__main__':
    app.run(port=5001, debug=True)