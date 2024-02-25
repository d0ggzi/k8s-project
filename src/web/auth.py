from .types import Response
from src.db import db
import jwt
from src.config import settings


def register_user(username, password):
    if not username or not password:
        return Response(400, "Username or password is required")
    res = db.reg_user(username, password)
    if res is False:
        return Response(400, "User with specified login already exists")
    encoded_jwt = jwt.encode({"userId": res}, settings.JWT_SECRET, algorithm="HS256")
    return Response(200, {"jwt": encoded_jwt}, [[b"content-type", b"application/json"]])


def login(username, password):
    if not username or not password:
        return Response(400, "Username or password is required")
    res = db.login(username, password)
    if res is False:
        return Response(400, "Invalid login or password")
    encoded_jwt = jwt.encode({"userId": res}, settings.JWT_SECRET, algorithm="HS256")
    return Response(200, {"jwt": encoded_jwt}, [[b"content-type", b"application/json"]])
