def to_json(objects) -> dict:
    objects["_id"] = str(objects["_id"])
    return objects
