from flask import Flask, request, jsonify
import bcrypt
from models import User, load_users, save_users

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    users = load_users()
    if any(user['username'] == data['username'] for user in users):
        return jsonify({"error": "User already exists"}), 400
    
    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(data['username'], data['email'], hashed_pw)
    users.append(new_user.to_dict())
    save_users(users)
    return jsonify({"message": "User registered successfully"}), 201

if __name__ == "__main__":
    app.run(port=5001, debug=True)