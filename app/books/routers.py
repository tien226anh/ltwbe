from functools import reduce
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Body
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.books.models import AddBookModel, RatingModel, UpdateModel, BookModel
from app.books.services import (
    count_books,
    create_book,
    find_books_by_filter_and_paginate,
    find_by_id,
    rating_book,
    update_book,
    find_books_not_paginate,
)
from app.user.services import get_user

# from fastapi_jwt_auth import AuthJWT

from db.init_db import get_collection_client

router = APIRouter()

client = get_collection_client("books")


@router.get("/")
async def get_books(
    title: str = "",
    author: str = "",
    category: str = "",
    skip: int = 1,
    limit: int = 10,
):
    query = {}
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if author:
        query["author"] = {"$regex": author, "$options": "i"}
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    books = await find_books_by_filter_and_paginate(query, skip, limit)
    count = await count_books(query)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"result": books, "total_record": count},
    )


@router.post("/")
async def add_new_book(body: AddBookModel):
    await create_book(body)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="Add new book successful"
    )


@router.get("/book/{id}")
async def get_detail(id: str):
    detail = await find_by_id(id)
    if detail:
        return JSONResponse(status_code=status.HTTP_200_OK, content=detail)
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not found")


@router.get("/book/rate/{id}")
async def get_book_rate(
    book_id: str,
):
    book = await find_by_id(book_id)
    all_rate = []
    for item in book["rating"]:
        all_rate.append(item["rate"])
    average_rate = reduce(lambda a, b: a + b, all_rate) / len(all_rate)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "average_rate": average_rate,
        },
    )


@router.get("/book/comment/{id}")
async def get_comment_rate(
    book_id: str,
):
    book = await find_by_id(book_id)
    all_comment = []
    for item in book["rating"]:
        user = await get_user(item["user_id"])
        print(user["username"])
        item["username"] = user["username"]
        all_comment.append(item)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "comment_rate": all_comment,
        },
    )


@router.post("/cover")
async def upload_cover(id: str, file: UploadFile = File(...)):
    book_id = ObjectId(id)
    try:
        content = await file.read()
        with open(f"static/bookscover/{file.filename}", "wb") as f:
            f.write(content)
    except Exception as error:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There was an error when uploading the file",
        )
    finally:
        await file.close()
    await update_book(book_id, {"cover": f"static/bookscover/{file.filename}"})
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=f"static/bookscover/{file.filename}",
    )


@router.put("/book/rate/{book_id}")
async def rate_book(
    book_id: str,
    rate_comment: RatingModel = Body(...),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    rate = rate_comment.rating
    comment = rate_comment.comment
    await rating_book(book_id, rate, comment, user_id)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="Successfull rate the book",
    )


# @router.get("/all")
# async def get_all(title: str = ""):
#     query = {}
#     if title:
#         query = {"title": {"$regex": f"{title}", "$options": "i"}}
#     books = await find_books_not_paginate(query)
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content=books,
#     )


@router.put("/{book_id}")
async def edit_book(book_id: str, data: UpdateModel = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    updated_book = await update_book(ObjectId(book_id), data)
    if updated_book is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=None)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)
