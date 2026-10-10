# Myntra Clone — Django Project

A Myntra-inspired e-commerce web application built using Python and Django.

## Features

- User registration and login
- Product listing and browsing
- Product images and categories
- Wishlist functionality
- User profile pages
- Django-based backend

*Note: Features depend on the functionality implemented in the current project.*

## Technologies Used

- Python
- Django
- HTML
- CSS
- SQLite
- Git and GitHub

## Project Structure

```text
Myntra/
├── manage.py
├── myntra_clone/
├── store/
├── templates/
├── static/
└── media/
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Kashish-s123/Myntra.git
cd Myntra
```

### 2. Create a virtual environment

```bash
python -m venv env
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

### 4. Install dependencies

Install the packages required by the project. If a `requirements.txt` file is available, run:

```bash
pip install -r requirements.txt
```

Otherwise, install Django and any other dependencies your project uses.

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open the following URL in your browser:

http://127.0.0.1:8000/

## Future Improvements

- Online payment integration
- Product search and filtering
- Shopping cart enhancements
- Responsive UI improvements

## Author

Kashish-s123

## License

This project is available for learning and educational purposes.