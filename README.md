#  ![Coderr Logo](assets/icons/logo_coderr.svg)  Backend API

This is a RESTful API backend for the Coderr platform, built with Django and Django REST Framework (DRF).
It supports user registration, authentication, business and customer profiles, offers, orders, and reviews for a service marketplace.

## Features
- User registration and token-based authentication
- Business and customer profile management
- CRUD operations for Offers and OfferDetails
- Order management for customers and businesses
- Review system for business users
- Permissions ensuring only authorized users can access or modify data
- Filtering, searching, and pagination for offers and reviews
- API schema and documentation support (optional, e.g. with drf-spectacular)

## Requirements
- Python 3.10+
- Django 5.2+
- Django REST Framework
- django-filter

## Setup & Installation

Clone the repository:

```bash
git clone <REPO_URL>
cd coderr_backend
```

Create and activate a virtual environment:

```bash
python3 -m venv env
source env/bin/activate  # macOS/Linux
# .\env\Scripts\activate # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser (optional, for admin access):

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

## Usage
- API base URL: `http://127.0.0.1:8000/api/`

### Authentication
Token-based authentication is used.
Obtain a token via the login endpoint.
Include the token in the Authorization header as:

```
Authorization: Token <your_token>
```

## Notes
- All endpoints (except registration and login) require authentication.
- Only business users can create offers; only customers can place orders and write reviews.
- Permissions are enforced for all sensitive operations.
- Filtering and searching are available for offers and reviews.

## About
This project provides the backend for a service marketplace platform, supporting business and customer interactions, offers, orders, and reviews.

---

© 2025 Coderr
