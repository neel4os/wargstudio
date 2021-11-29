import json
import datetime
from bson import ObjectId
from pydantic.utils import Obj


class MongoDbOrganizaionEncoder(json.JSONEncoder):
    def default(self, obj):
        print(type(obj))
        if isinstance(obj, datetime.datetime):
            return obj.astimezone().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
