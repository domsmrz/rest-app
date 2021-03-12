from flask import Blueprint
from flask_restful import Resource, Api
from typing import Callable, Type


blueprint = Blueprint('view', __name__)
api = Api(blueprint)


def api_route_resource(*routes: str) -> Callable[[Type[Resource]], Type[Resource]]:
    def wrapper(cls: Type[Resource]) -> Type[Resource]:
        api.add_resource(cls, *routes)
        return cls
    return wrapper
