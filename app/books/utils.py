# def to_json(objects) -> dict:
#     objects["_id"] = str(objects["_id"])
#     return objects

from bson import ObjectId
import json


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


def to_json(objects) -> dict:
    return json.loads(json.dumps(objects, cls=CustomJSONEncoder))
