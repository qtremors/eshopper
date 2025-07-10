# EShopper - Django E-commerce Platform

EShopper is a feature-rich e-commerce platform built with Django. It provides a complete online shopping experience, from browsing products to a secure checkout process. This project is designed to be a robust and scalable solution for online retail.

## Features

* **Product Catalog**: Browse products by category and sub-category.
* **Search and Filter**: Easily find products with search and price filtering options.
* **Shopping Cart**: Add products to a cart, update quantities, and apply coupon codes.
* **Wishlist**: Save products for later purchase.
* **User Authentication**: Secure user registration, login, and profile management.
* **Order Management**: Place orders and view order history.
* **Product Reviews**: Leave reviews and ratings for products.
* **Responsive Design**: A mobile-friendly interface for a seamless experience on any device.

## Tech Stack

* **Backend**: Django
* **Frontend**: HTML, CSS, Bootstrap
* **Database**: SQLite (or any other Django-supported database)

## Getting Started

### Prerequisites

* Python 3.x
* Django
* Pillow (for image handling)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/your-username/eshopper.git](https://github.com/your-username/eshopper.git)
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Run the development server**:
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`.

## Project Structure

* `models.py`: Defines the database schema for products, categories, users, orders, etc.
* `views.py`: Contains the business logic for handling requests and rendering templates.
* `urls.py`: Maps URLs to their corresponding views.
* `templates/`: Contains the HTML templates for the user interface.

## Contributing

Contributions are welcome! If you have any suggestions or find any bugs, please open an issue or submit a pull request.
