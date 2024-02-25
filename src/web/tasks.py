from .types import Response
from src.db import db
import uuid


def is_admin(user_id: int) -> bool:
    return db.is_admin(user_id)


def is_right_csrf(csrf_token: str, user_id: int) -> bool:
    return csrf_token == db.get_csrf_by_id(user_id)


def admin_get_task_lists(user_id) -> Response:
    res, message = db.admin_get_task_lists()
    status_code = 200 if res else 400
    csrf_token = str(uuid.uuid4())
    message = [message, csrf_token]
    db.store_csrf_token(user_id, csrf_token)
    return Response(status_code, message, [[b"content-type", b"application/json"]])


def admin_get_tasks(task_list_name: str) -> Response:
    res, message = db.admin_get_tasks(task_list_name)
    status_code = 200 if res else 400
    return Response(status_code, message, [[b"content-type", b"application/json"]])


def create_task_list(task_list_name: str, user_id: int) -> Response:
    res, message = db.create_task_list(task_list_name, user_id)
    status_code = 200 if res else 400
    return Response(status_code, message)


def get_task_lists(user_id: int) -> Response:
    res, message = db.get_task_lists(user_id)
    status_code = 200 if res else 400
    csrf_token = str(uuid.uuid4())
    message = [message, csrf_token]
    db.store_csrf_token(user_id, csrf_token)
    return Response(status_code, message, [[b"content-type", b"application/json"]])


def update_task_list(
    task_list_old_name: str, task_list_new_name: str, user_id: int
) -> Response:
    res, message = db.update_task_list(task_list_old_name, task_list_new_name, user_id)
    status_code = 200 if res else 400
    return Response(status_code, message)


def delete_task_list(task_list_name: str, user_id: int) -> Response:
    res, message = db.delete_task_list(task_list_name, user_id)
    status_code = 200 if res else 400
    return Response(status_code, message)


def create_task(
    task_list_name: str, task_name: str, description: str, user_id: int
) -> Response:
    res, message = db.create_task(task_list_name, task_name, description, user_id)
    status_code = 200 if res else 400
    return Response(status_code, message)


def get_tasks(task_list_name: str, user_id: int) -> Response:
    res, message = db.get_tasks(task_list_name, user_id)
    status_code = 200 if res else 400
    return Response(status_code, message, [[b"content-type", b"application/json"]])


def update_task(
    task_old_name: str,
    task_new_name: str,
    new_desc: str,
    task_list_name: str,
    user_id: int,
) -> Response:
    res, message = db.update_task(
        task_old_name, task_new_name, new_desc, task_list_name, user_id
    )
    status_code = 200 if res else 400
    return Response(status_code, message)


def delete_task(task_name: str, task_list_name: str, user_id: int) -> Response:
    res, message = db.delete_task(task_name, task_list_name, user_id)
    status_code = 200 if res else 400
    return Response(status_code, message)
