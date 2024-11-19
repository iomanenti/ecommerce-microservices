import unittest
import requests_mock
import requests

class TestOrderService(unittest.TestCase):
    ORDER_SERVICE_URL = "http://localhost:5004"

    def setUp(self):
        self.order_data = {
            "user_id": "testuser",
            "items": [
                {"product_id": 1, "name": "Test Product", "price": 100.0, "quantity": 1}
            ],
            "total_price": 100.0
        }

    @requests_mock.Mocker()
    def test_place_order(self, mock):
        # Mock the place order endpoint
        mock.post(f"{self.ORDER_SERVICE_URL}/order", json={"message": "Order placed successfully"}, status_code=201)

        # Send a POST request to place an order
        response = requests.post(f"{self.ORDER_SERVICE_URL}/order", json=self.order_data)

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Order placed successfully")

    @requests_mock.Mocker()
    def test_place_order_invalid_data(self, mock):
        # Mock the place order endpoint with invalid data
        mock.post(f"{self.ORDER_SERVICE_URL}/order", json={"error": "Invalid order data"}, status_code=400)

        # Send a POST request with invalid order data
        response = requests.post(f"{self.ORDER_SERVICE_URL}/order", json={})

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid order data")


### TestProductService class  ###

class TestProductService(unittest.TestCase):
    PRODUCT_SERVICE_URL = "http://localhost:5002"

    def setUp(self):
        self.product_data = {
            "name": "Test Product",
            "description": "A product for testing",
            "price": 100.0,
            "stock": 10
        }

    @requests_mock.Mocker()
    def test_add_product(self, mock):
        # Mock the add product endpoint
        mock.post(f"{self.PRODUCT_SERVICE_URL}/products", json={"message": "Product added successfully"}, status_code=201)

        # Send a POST request to add a product
        response = requests.post(f"{self.PRODUCT_SERVICE_URL}/products", json=self.product_data)

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Product added successfully")

    @requests_mock.Mocker()
    def test_add_product_missing_fields(self, mock):
        # Mock the add product endpoint with missing fields
        mock.post(f"{self.PRODUCT_SERVICE_URL}/products", json={"error": "Invalid product data"}, status_code=400)

        # Send a POST request with invalid data
        response = requests.post(f"{self.PRODUCT_SERVICE_URL}/products", json={})

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid product data")

### TestUserService class  ###

class TestUserService(unittest.TestCase):
    USER_SERVICE_URL = "http://localhost:5001"

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "is_admin": False
        }

    @requests_mock.Mocker()
    def test_user_registration(self, mock):
        # Mock the registration endpoint
        mock.post(f"{self.USER_SERVICE_URL}/register", json={"message": "User registered successfully"}, status_code=201)

        # Send a POST request to register a user
        response = requests.post(f"{self.USER_SERVICE_URL}/register", json=self.user_data)

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "User registered successfully")

    @requests_mock.Mocker()
    def test_user_registration_duplicate(self, mock):
        # Mock the registration endpoint to simulate duplicate user
        mock.post(f"{self.USER_SERVICE_URL}/register", json={"error": "Username already exists"}, status_code=400)

        # Send a POST request to register a duplicate user
        response = requests.post(f"{self.USER_SERVICE_URL}/register", json=self.user_data)

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Username already exists")