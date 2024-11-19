Simple E-commerce with Microservices
=====================================
<br>

The project is divided into multiple microservices, each handling specific responsibilities (e.g., user management, product management, cart, and orders). A simple frontend integrates these services.
<br>

        |-- ecommerce-microservices/

        |-- user_controller.py         # Manages user registration and authentication

        |-- product_controller.py      # Handles product addition, editing, and listing

        |-- cart_controller.py          # Manages the shopping cart functionality

        |-- order_controller.py        # Processes and records orders
    
        |-- frontend/              # Simple black and white frontend using Flask templates

        |-- tests/                # Unit testing for the vital application usage

        |-- docker-compose.yml     # For running all services

        |-- README.md

<br>

# Using Microservices Architecture on this E-commerce
</br>
Microservices architecture offers significant advantages for building scalable and maintainable applications. By dividing the application into smaller, self-contained services, it enables independent development, testing, and deployment of each component. Microservices enhance fault isolation, ensuring that a failure in one service does not impact the entire system, while also improving scalability by allowing individual services to be scaled based on demand. Overall, microservices architecture is ideal for complex systems requiring agility, scalability, and ease of maintenance.
</br>
![Alt text](images/simple_ecommerce_microservices_architecture.jpg)
</br>

# Using the Simple E-commerce
</br>

## Login Screen
</br>
On this screen you can use to login with a registered user:
</br>
![Alt text](images/login-screen.jpg)

</br>

## Register Screen
</br>
On this screen you can register a new user and choose if it is and admin or not:
</br>
![Alt text](images/register-screen.jpg)

</br>

## Product Screen as an Regular User
</br>
Once you had logged in as a regular user you can choose the product and add to the cart with the quantity as you wanted.
</br>
![Alt text](images/regular-product-screen.jpg)

</br>

## Product Screen as an Admin User
</br>
Once you had logged in as a admin user you can choose the product and add to the cart with the quantity as you wanted but also edit product and delete product from the catalog.
</br>
![Alt text](images/admin-product-screen.jpg)

</br>

## Cart Screen
</br>
On this screen you can remove itens to your cart and also place your order. You cart is saved until you place an order.
</br>
![Alt text](images/cart-screen.jpg)

</br>