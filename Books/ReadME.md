# FastAPI Bookstore API

A simple FastAPI-based API for managing a collection of books. This API allows users to retrieve, add, update, and delete books using various endpoints.

## Features

- GET books by title, author, or category
- POST new books to the collection
- PUT update existing book details
- DELETE remove a book from the collection

## Installation

Clone this repository:

```bash
git clone https://github.com/anandreddy05/FastAPI.git
cd Books
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

### Future Improvements

- Add a database for persistent storage
- Implement authentication and authorization
- Add pagination for large datasets
