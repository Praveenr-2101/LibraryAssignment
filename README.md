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

Brief explanation of my approach.

1. Separation of Concerns
Views handle CRUD operations for entities like Author, Book, and BorrowRecord.
Serializers validate and transform data, including custom checks like available_copies in books.
Impelement signals post_save() for borrow item 

3. APIView Usage
APIView explicitly defines methods (get, post, put, delete) for better control.
Example: AuthorList manages listing and creating authors, while AuthorDetail handles specific author operations.

4. Validation and Error Handling
Custom validations, like verifying available_copies, are implemented in serializers.
try-except blocks in views handle exceptions, returning appropriate responses (e.g., 404 for missing resources)

5. JWT Authentication
rest_framework_simplejwt secures endpoints with token-based authentication.
Login and token refresh are managed via TokenObtainPairView and TokenRefreshView.

6. Asynchronous Task for Report Generation
Celery processes tasks like generate_report.delay() asynchronously.
Reports are stored in a directory and served efficiently using FileResponse.

7. Test Cases
Test cases validate API functionality, such as creating authors or borrowing records.
setUp initializes test data and handles JWT authentication for assertions.

8. URL Routing
URLs are logically grouped for entities like Author, Book, and reports.
JWT token endpoints for login and refresh are included.

9. Custom Serialization Logic
BookSerializer supports nested serialization and custom create/update methods.
This ensures seamless handling of relationships and data integrity.

10. Permissions
IsAuthenticated restricts access to authenticated users, ensuring secure endpoints.
This adheres to REST principles and best practices.

