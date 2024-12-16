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
- PostgreSQL (or your preferred database)
- Redis (for Celery)
- Virtual Environment (venv)

### Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/library-management.git
   cd library-management
