from typing import Optional
from pydantic import BaseModel


class BookModel(BaseModel):
    title: str
    author: str
    describe: Optional[str]
    release_date: Optional[str]
    page_number: Optional[int]
    category: Optional[str]
    cover: Optional[str]
    price: Optional[int]


class AddBookModel(BaseModel):
    title: str
    author: str
    describe: str
    release_date: str
    page_number: int
    category: str
    price: int


class UpdateModel(BaseModel):
    title: str
    author: str
    describe: Optional[str]
    release_date: Optional[str]
    page_number: Optional[int]
    category: Optional[str]
    cover: Optional[str]
    price: Optional[int]


class RatingModel(BaseModel):
    rating: float
    comment: str
