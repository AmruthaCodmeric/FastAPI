from fastapi import Body, FastAPI
app = FastAPI() #this allows uvicorn identify that we are creating a new app of fastapi and is importing all the resource importing from above code

BOOKS = [
         {'Title':'Title one', 'Author':'Author one', 'Category':'Science'},
         {'Title':'Title two', 'Author':'Author two', 'Category':'Science'},
         {'Title':'Title three', 'Author':'Author one', 'Category':'History'},
         {'Title':'Title four', 'Author':'Author four', 'Category':'Math'},
         {'Title':'Title five', 'Author':'Author one', 'Category':'Math'},
         {'Title':'Title six', 'Author':'Author six', 'Category':'Math'}


]
@app.get("/books")
#async python function
async def read_all_books():
 return BOOKS
 #return{"message" : "hello maya"}

"""@app.get("/books/mybook")
async def read_all_books():
    return {'book_title':'my favourite book'}"""

#PATH PARAMETER
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('Title').casefold() == book_title.casefold():
            return book

#QUERY PARAMETER

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('Category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

#FETCHING AUTHOR AND FILTER BY CATEGORY
@app.get("/books/{book_author}/")
async def read_author_category_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('Author').casefold() == book_author.casefold() and \
                book.get('Category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

#POST

@app.post("/books/create_book")
async def create_book(new_book=Body()):
  BOOKS.append(new_book)


#PUT

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range (len(BOOKS)):
        if BOOKS[i].get('Title').casefold() == updated_book.get('Title').casefold():
            BOOKS[i]= updated_book


#DELETE


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range (len(BOOKS)):
        if BOOKS[i].get('Title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


#ASSIGNMENT -Create a new API Endpoint that can fetch all books from a specific author using either Path Parameters or Query Parameters.
#Path Parameters

@app.get("/books/byauthor/{author_name}")
async def read_book_author( author_name: str ):
    books_to_returns =[]
    for book in BOOKS:
        if book.get('Author').casefold() == author_name.casefold():
            books_to_returns.append(book)
    return books_to_returns

#Query Parameters

@app.get("/books/byauthor/author/")
async def read_book_author( author_name: str ):
    books_to_returns =[]
    for book in BOOKS:
        if book.get('Author').casefold() == author_name.casefold():
            books_to_returns.append(book)
    return books_to_returns

