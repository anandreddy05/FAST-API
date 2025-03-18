from fastapi import Body,FastAPI

app = FastAPI()

BOOKS = [
    {'title':'Title 1','author':"Author 1",'category':'science'},
    {'title':'Title 2','author':"Author 2",'category':'science'},
    {'title':'Title 3','author':"Author 3",'category':'history'},
    {'title':'Title 4','author':"Author 1",'category':'history'},
    {'title':'Title 5','author':"Author 2",'category':'math'},
    {'title':'Title 6','author':"Author 2",'category':'math'},
]

# Get Request

@app.get("/books")
async def get_books():
    return BOOKS

# @app.get("/books/my_book")
# async def get_books():
#     return {"my_book":"my favourite book"}

@app.get("/books/{book_title}")
async def read_all_books(book_title:str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
        
@app.get("/books/")
async def read_all_books_by_query(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/byauthor/")
async def read_books_by_author(author:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get('/books/{author_name}/')
async def read_books_by_author_and_category(author_name:str,category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author_name.casefold() and \
           book.get("category").casefold() == category.casefold():
               books_to_return.append(book)
    return books_to_return

# Post Request

    
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    
# Put Request

@app.put("/books/update_book") 
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break 
