# FastAPI TODOS Application

This repository contains a FastAPI-based application designed to manage a simple TODO list.

The application provides endpoints to create, read, update, and delete TODO items, offering a straightforward example of building RESTful APIs with FastAPI.

## Features

- CRUD Operations: Perform Create, Read, Update, and Delete operations on TODO items.​
- SQLite Integration: Utilizes SQLite for data storage, ensuring a lightweight and easy-to-set-up database solution.​
- Pydantic Models: Employs Pydantic for data validation and serialization, ensuring data integrity and automatic documentation generation.​
- Interactive API Documentation: Access automatically generated Swagger UI at /docs and ReDoc at /redoc for interactive API exploration.​

## Installation

Clone the Repository:

```bash
Edit
git clone https://github.com/anandreddy05/FAST-API.git
cd FAST-API/TODOS
```

Create and Activate a Virtual Environment:

On macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

On Windows:

```bash
python -m venv env
.\env\Scripts\activate
```

## Install Dependencies:

``` bash
pip install fastapi==0.115.8 uvicorn[standard]==0.34.0 SQLAlchemy==2.0.38 pydantic==2.10.6 python-jose==3.3.0 passlib[bcrypt]==1.7.4
```

## Running the Application

After installing the dependencies:

```bash
uvicorn main:app --reload
```

The application will be accessible at <http://127.0.0.1:8000//>

## Project Structure

- main.py: Contains the FastAPI application with route definitions for managing TODO items.​
- models.py: Defines the Pydantic models and SQLAlchemy ORM models representing the TODO items.​
- database.py: Sets up the SQLite database connection and initializes the database tables.​

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
