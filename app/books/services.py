from typing import Optional

from bson import ObjectId
from fastapi import HTTPException, status

from app.books.utils import to_json
from db.init_db import get_collection_client

client = get_collection_client("books")


async def create_book(book):
    book_dict = book.dict()
    existing_book = await client.find_one({"title": book_dict["title"]})
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Book already exist",
        )
    created_book = await client.insert_one(book_dict)
    return await client.find_one({"id": created_book.inserted_id})


async def update_book(book_id: ObjectId, book):
    return await client.update_one({"_id": book_id}, {"$set": book})


async def find_by_id(id: str) -> dict:
    book_detail = await client.find_one({"_id": ObjectId(id)})
    if book_detail:
        book = to_json(book_detail)
        return book


async def find_books_by_filter_and_paginate(
    filter_books,
    skip: int,
    limit: int,
):
    offset = (skip - 1) * limit if skip > 0 else 0
    books = []
    async for book in client.find(filter_books).sort("_id").skip(offset).limit(limit):
        book = to_json(book)
        books.append(book)
    return books


async def find_books_not_paginate(filter_books):
    books = []
    async for book in client.find(filter_books).sort("_id"):
        book = to_json(book)
        books.append(book)
    return books


async def count_books(filter_books):
    return await client.count_documents(filter_books)


def book_entity(book):
    return {
        "_id": str(book["_id"]),
        "title": str(book["title"]),
        "author": str(book["author"]),
        "describe": str(book["describe"]),
        "release_date": str(book["release_date"]),
        "page_number": str(book["page_number"]),
        "category": str(book["category"]),
        "cover_url": str(book["cover_url"]),
        "price": str(book["price"])
    }
