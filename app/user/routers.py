from typing import Union, List
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.auth.password import get_password_hash
from app.user.models import Role, UserCreateModel, UserUpdateModel
from app.user.services import (
    count_users,
    create_user,
    delete_user,
    find_user_by_id,
    get_users,
    update_user,
    user_entity,
    add_book_cart,
)
from db.init_db import get_collection_client

router = APIRouter()

client = get_collection_client("users")


@router.post("/")
async def create_new_user(body: UserCreateModel):
    user_dict = body.dict()

    existing_user = await client.find_one({"username": user_dict["username"]})

    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content="User already exist"
        )
    user_dict["hashed_password"] = get_password_hash(user_dict["password"])
    user_dict.pop("password")
    await create_user(user_dict)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content="Succesful create new user"
    )


@router.get("/me")
async def get_me(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user = await find_user_by_id(ObjectId(user_id))
    if user is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=None)

    return JSONResponse(status_code=status.HTTP_200_OK, content=user_entity(user))


@router.get("/")
async def get_all(
    name="",
    role: Union[Role, None] = None,
    authorize: AuthJWT = Depends(),
    skip=0,
    limit=20,
):
    authorize.jwt_required()

    query = {
        "$or": [
            {"full_name": {"$regex": f"\\b{name}\\b", "$options": "i"}},
            {"full_name": {"$regex": name, "$options": "i"}},
            {"username": {"$regex": f"\\b{name}\\b", "$options": "i"}},
            {"username": {"$regex": name, "$options": "i"}},
        ]
    }

    if role is not None:
        query["$and"] = [{"role": role}]

    users = await get_users(query, int(skip), int(limit))
    count = await count_users(query)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"result": users, "total_record": count}
    )


@router.put("/me")
async def update_me(
    user_data: UserUpdateModel = Body(...), authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    user_id = ObjectId(authorize.get_jwt_subject())

    user_data = {k: v for k, v in user_data.dict().items() if v is not None}
    updated_user = await update_user(user_id, user_data)
    if updated_user is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=None)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.put("/{id}")
async def update_by_id(id: str, user_data: UserUpdateModel = Body(...)):
    user_data = {k: v for k, v in user_data.dict().items() if v is not None}
    updated_user = await update_user(ObjectId(id), user_data)
    if updated_user is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=None)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content="Successful edit")


@router.delete("/{id}")
async def delete(id: str):
    deleted = await delete_user(id)
    if deleted is not True:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=None)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.post("/cart")
async def add_cart(books: List[str] = Body(...), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    id_obj = ObjectId(authorize.get_jwt_subject())
    list_books = []
    for item in books:
        list_books.append(ObjectId(item))
    await add_book_cart(id_obj, list_books)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="Successful add to cart"
    )


@router.post("/avatar")
async def upload_avatar(file: UploadFile = File(...), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = ObjectId(authorize.get_jwt_subject())
    try:
        content = await file.read()
        with open(f"static/avatar/{file.filename}", "wb") as f:
            f.write(content)
    except Exception as error:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There was an error when trying uploading the file",
        )
    finally:
        await file.close()
    await update_user(user_id, {"avatar": f"static/avatar/{file.filename}"})
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=f"static/avatar/{file.filename}",
    )
