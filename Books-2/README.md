# FastAPI Bookstore API - 2

This is a simple **FastAPI** application that provides an API for managing books. It includes features like retrieving books, searching by rating, filtering by published date, adding new books, updating book details, and deleting books.

---

## Features

- Retrieve all books 📖
- Get a specific book by ID 🔍
- Filter books by rating ⭐
- Filter books by published date 📅
- Add a new book ➕
- Update a book's details ✏️
- Delete a book ❌

---

## Installation & Setup

### Clone the repository

```bash
git clone https://github.com/anandreddy05/FastAPI.git
cd Books-2
```

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activatesource  #On Mac we use venv/bin/activate 
```

Install dependencies:

```bash
pip install fastapi[standard] uvicorn[standard]
```

Run the API server:

```bash
uvicorn main:app --reload
```

The API will be available at: <http://127.0.0.1:8000/>

## Notes

- The API uses Pydantic for request validation.
- All books have a rating between 1 to 5.
- Books should have a published date between 2000 and 2024.
- The API provides automatic interactive documentation at:
- Swagger UI: <http://127.0.0.1:8000/docs/>
- Redoc: <http://127.0.0.1:8000/redoc/>