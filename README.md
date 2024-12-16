# Library Management System

This project is a Django-based Library Management System that allows users to manage authors, books, and borrowing records. It includes APIs for creating and retrieving records, token-based authentication, reporting, and asynchronous task handling with Celery.

---

## Features
- Manage authors and books.
- Borrow and return books with availability updates.
- Generate token-based authentication.
- Celery integration for asynchronous tasks.

---

## Steps to Run the Project

### Prerequisites
Ensure the following are installed:
- Python 3.8+
- Django 4.x
- Redis (for Celery)
- Virtual Environment (venv)

### Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/library-management.git
   cd library-management


##Run Project

```bash
   cd Library
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   cd Library
   python manage.py runserver
```

##Celery setup

```
   pip install celery[redis]

   setting configuration of celery

   proj/proj/celery.py
      -Configuring Celery for Asynchronous Task Handling in Django

   proj/proj/__init__.py
      -Initializing Celery Integration with the Django Project

   app/task.py
      -Using the @shared_task decorator create task

   Trigger tasks in views.py:
      - celery will run background once it trigger the task
```
##celery Worker
```
   celery -A proj worker -l INFO
```


###Docker Image container

```
   pip freeze > requirements.txt

   Create a Dockerfile
      -Setting Up the Docker Environment for Django Application

   Create a docker-compose.yml
      -Multi-Container Setup for Django and db

   Build the containers:
      -docker-compose build

   Run the containers:
      -docker-compose up
```   


