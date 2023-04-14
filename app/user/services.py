import re
from typing import List

from bson.objectid import ObjectId

# from app.list_object.service import object_to_json
from app.user.models import InterestedModel
from db.init_db import get_collection_client

client = get_collection_client("users")


async def create_user(user):
    created_user = await client.insert_one(user)
    return await client.find_one({"id": created_user.inserted_id})


async def read_user_by_username(username: str):
    return await client.find_one({"username": username})


async def update_user(user_id: ObjectId, user):
    return await client.update_one({"_id": user_id}, {"$set": user})


async def delete_user(user_id: str):
    user = await client.delete_one({"_id": ObjectId(user_id)})
    if user:
        await client.delete_one({"_id": ObjectId(user_id)})
        return True


async def get_users(filter_spec, skip: int, limit: int):
    offset = (skip - 1) * limit if skip > 0 else 0
    users = []
    async for new in client.find(filter_spec).sort("_id").skip(offset).limit(limit):
        new = user_entity(new)
        users.append(new)

    return users


async def count_users(filter_spec):
    return await client.count_documents(filter_spec)


async def get_user_by_id(id: ObjectId):
    return await client.find_one({"_id": id})


async def get_user(id: str) -> dict:
    users = await client.find_one({"_id": ObjectId(id)})
    if users:
        return user_entity(users)


async def find_user_by_id(user_id: str):
    return await client.find_one({"_id": user_id})


def user_entity(user) -> dict:
    return {
        "_id": str(user["_id"]),
        "email": user["email"],
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"],
        "avatar_url": user["avatar_url"] if "avatar_url" in user else None,
    }
