# Hospital Management System

This project is a web-based application developed using the Django web framework. It is designed to manage various functionalities of a hospital including user authentication, appointments, staff management, room booking, ICU medicine management, doctor-related functionalities, and live search from the database for medicines.

## Features

- **User Authentication**: Register, login, logout, password reset
- **CRUD Operations**:
  - Appointments
  - Staff
  - Room booking
  - ICU medicine
  - Doctor details
- **Live Search**: Real-time search functionality for medicines



## Technologies Used

- Python
- Django
- PostgreSQL
- jQuery
- JavaScript
- Bootstrap
- HTML


## Install Python

```bash
    sudo apt install python3
```

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ayushipandya89/Hospital-Management-System.git
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

7. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:8000/`
