from .auth import register_user, login
from .tasks import (
    create_task_list,
    create_task,
    get_tasks,
    get_task_lists,
    update_task_list,
    update_task,
    delete_task_list,
    delete_task,
    is_admin,
    admin_get_task_lists,
    admin_get_tasks,
    is_right_csrf,
)
import jwt
from .types import Response
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
from src.config import settings


def verify_jwt(user_jwt: str) -> int:
    encoded = jwt.decode(user_jwt, settings.JWT_SECRET, algorithms="HS256")
    user_id = encoded["userId"]
    return user_id


def parse_headers(headers: dict) -> dict:
    new_headers = {}
    for key, value in headers:
        new_headers[key.decode("utf-8")] = value.decode("utf-8")
    return new_headers


class RequestParser:
    def __init__(self, body, method, path, headers) -> None:
        self.body = body
        self.method = method
        if path.startswith("/api"):
            path = path[4:]
        self.path = path
        self.headers = parse_headers(headers)

    def parse(self) -> Response:
        if self.method == "OPTIONS":
            return Response(status_code=204, body="")

        if self.method == "POST" and self.path == "/auth/reg":
            return register_user(self.body["username"], self.body["password"])
        elif self.method == "POST" and self.path == "/auth/login":
            return login(self.body["username"], self.body["password"])
        else:
            try:
                jwt_token = self.headers["authorization"]
                user_id = verify_jwt(jwt_token)
            except (
                KeyError,
                ExpiredSignatureError,
                InvalidSignatureError,
                DecodeError,
            ) as e:
                print(e)
                return Response(status_code=401, body="Unauthorized")

            if is_admin(user_id) and self.method == "GET" and self.path == "/task_list":
                return admin_get_task_lists(user_id)
            elif is_admin(user_id) and self.method == "GET" and self.path == "/task":
                return admin_get_tasks(self.body["task_list_name"])

            if (
                self.method == "POST"
                and self.path == "/task_list"
                and is_right_csrf(self.headers["x-csrf-token"], user_id)
            ):
                return create_task_list(self.body["task_list_name"], user_id)
            elif self.method == "GET" and self.path == "/task_list":
                return get_task_lists(user_id)
            elif self.method == "PUT" and self.path == "/task_list":
                return update_task_list(
                    self.body["task_list_old_name"],
                    self.body["task_list_new_name"],
                    user_id,
                )
            elif self.method == "DELETE" and self.path == "/task_list":
                return delete_task_list(self.body["task_list_name"], user_id)

            elif (
                self.method == "POST"
                and self.path == "/task"
                and is_right_csrf(self.headers["x-csrf-token"], user_id)
            ):
                return create_task(
                    self.body["task_list_name"],
                    self.body["task_name"],
                    self.body["description"],
                    user_id,
                )
            elif self.method == "GET" and self.path == "/task":
                return get_tasks(self.body["task_list_name"], user_id)
            elif self.method == "PUT" and self.path == "/task":
                return update_task(
                    self.body["task_old_name"],
                    self.body["task_new_name"],
                    self.body["new_desc"],
                    self.body["task_list_name"],
                    user_id,
                )
            elif self.method == "DELETE" and self.path == "/task":
                return delete_task(
                    self.body["task_name"], self.body["task_list_name"], user_id
                )
        return Response(status_code=404, body="Method Not Allowed")
