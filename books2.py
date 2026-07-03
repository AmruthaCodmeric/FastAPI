from dataclasses import field
from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

#pydantic is the framework that allow  as to do the validation on data , BaseModel pydantic object
#fields will allow as to be able to add validation to each field of that request object
app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date : int
    def __init__(self,id,title,author,description, rating, published_date):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        self.published_date=published_date
# basemodel(parent class) , to validate the variables ,new object bookrequest is used to validate the book requests then it's added to books list
class BookRequest(BaseModel):
   #id:Optional[int] = None   id can be int/null
   id: Optional[int] = Field(description='ID is not needed on create', default=None)
   title:str =Field(min_length=3)
   author:str =Field(min_length=1)
   description:str =Field(min_length=1, max_length=100)
   rating:int =Field(gt=0 ,lt=6)
   published_date: int =Field(gt=1998 ,lt=2026)

# model_congif should be inside the pydantic book request
   model_config = {
       "json_schema_extra": {
           "example": {
               "title": "a new book",
               "author": "codingwithroby",
               "description": "a new description of a book",
               "rating": 5
           }
       }
   }

BOOKS =[
    Book(1,"Computer Science","robi", "a very nice book", 5,2023),
    Book(2,"Fast API","robi", "a very nice book", 5, 2012),
    Book(3,"Master Endpoint","robi", "a very nice book", 5, 2014),
    Book(4,"HP1","Author1", "Book Description", 2, 2007),
    Book(5,"HP2","Author2", "Book Description", 3, 1999),
    Book(6,"HP3","Author3", "Book Description", 1, 2012),
        ]
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(rating: int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating== rating:
           books_to_return.append(book)
    return books_to_return

@app.get("/books/publisheddate/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(book_publish_date:int = Query(gt=1998 ,lt=2026)):
    books_published = []
    for book in BOOKS:
        if book.published_date == book_publish_date:
           books_published.append(book)
    return books_published


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
#can't do validation on Body()
async def create_book(book_request:BookRequest):
   # print(type(book_request)) type is BookRequest(cls)
   #BOOKS.append(book_request) model_dump/dict() Returns a dictionary or key-value pair and ** allow as to assign those in to our keyword arguments
   #transform the book request in to actual book
   new_book = Book(**book_request.model_dump())
   #print(type(new_book)) # type is Book(cls)
   #BOOKS.append(new_book)
   BOOKS.append(find_book_id(new_book))

def find_book_id(book:Book):
   """ if len(BOOKS)>0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1"""
   book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id +1
   return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


"""@app.delete("/books/delete_book/")
async def delete_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS.pop(i)"""

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT
            )
async def delete_book(book_id:int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')
