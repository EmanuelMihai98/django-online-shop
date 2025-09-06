# Django Online Shop

A fully functional online shop backend built with Django \& Django REST Framework.  

Features cart management with session storage, orders, user authentication, and secure password handling.



---



## Features

- User authentication (register, login, logout, change password)

- Product management (list, create, update, delete)

- Cart functionality (add, remove, decrease, timestamp ordering)

- Orders (create, cancel, detail view)

- RESTful API with DRF

- 100% test coverage for Products, Cart, Orders, and Users



---



## Installation \& Usage



Clone the repository:



```bash

git clone https://github.com/EmanuelMihai98/django-online-shop.git

cd django-online-shop

```

---


## Create a virtual environment and install dependencies:



```bash

python -m venv venv

source venv/bin/activate   # Linux/Mac

venv\\Scripts\\activate      # Windows

pip install -r requirements.txt

```

---





## Apply migrations and run server:



```bash

python manage.py migrate

python manage.py runserver

```

---


## Running tests



Run all tests:



```bash

python manage.py test -v 2

```

Run individual tests (example for products):



```bash

python manage.py test tests.tests\_products -v 2

```

---



## Project structure:



- products/ → product model, serializer, API



- cart/ → session-based cart with timestamp ordering



- orders/ → order creation and cancellation, order details and order pay (update Status from "Pending" to "Paid")



- users/ → user registration, login, logout, change password



- tests/ → central folder with separated test files



---




## Future improvements



- Switch to PostgreSQL for production



- Dockerize app for easier deployment



- Add payment integration (Stripe)



