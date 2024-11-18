Simple E-commerce with Microservices
=====================================

The project is divided into multiple microservices, each handling specific responsibilities (e.g., user management, product management, cart, and orders). A simple frontend integrates these services.

|-- ecommerce-microservices/

        |-- user_controller.py         # Manages user registration and authentication

        |-- product_controller.py      # Handles product addition, editing, and listing

        |-- cart_controller.py          # Manages the shopping cart functionality

        |-- order_controller.py        # Processes and records orders
    
        |-- frontend/              # Simple black and white frontend using Flask or Django templates

        |-- shared/                # Common utilities (e.g., authentication checks)

        |-- docker-compose.yml     # For running all services

        |-- README.md


***Using Microservices Architecture on this E-commerce***
![Alt text](images/simple_ecommerce_microservices_architecture.jpg)
