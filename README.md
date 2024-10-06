# E-commerce App

This is a simple and responsive e-commerce application built using Django Rest Framework. The app was developed with the assistance of Claude, an AI language model.

## Features

### Product List
- Displays a list of products fetched from the fakestoreapi.com
- Allows sorting of products by price:
  - Price low to high
  - Price high to low
- Each product card includes an "Add to Cart" button

### Shopping Cart
- Lists items added to the cart
- Allows users to change the quantity of each item in the cart
- Calculates and displays the total price of all items in the shopping cart

### Payment
- Integrates Stripe payment system for secure transactions

## Technical Stack

- Backend: Python (Django Rest Framework)
- Payment Integration: Stripe

## Setup and Installation

(Include instructions for setting up the project, such as:)

1. Clone the repository
2. Install backend dependencies
3. Set up the database
5. Configure environment variables (Add .env file in root directory)
    a. Add STRIPE_PUBLISHABLE_KEY
    b. Add STRIPE_SECRET_KEY
6. Run the development servers

## API Endpoints

(List and briefly describe the main API endpoints, for example:)

- `GET /api/products/`: Retrieve list of products
- `GET /api/products/?sort_by_price`: Get products sorted by price (low to high)
- `GET /api/products/sort_by_price/?order=desc`: Get products sorted by price (high to low)
- `POST /api/cart/`: Add item to cart
- `GET /api/cart/`: Retrieve cart contents
- `PUT /api/cart/{id}/`: Update cart item quantity
- `POST /api/payment/create-charge/`: Process payment with Stripe

## Acknowledgements

This project was developed with the assistance of Claude, an AI language model created by Anthropic. Claude provided guidance on implementing the backend services using Django Rest Framework, integrating with fakestoreapi.com for product data, and setting up the Stripe payment integration.



