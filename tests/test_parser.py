import json

import pytest

from src.web.parser import RequestParser
from src.web.types import Response
import uuid


@pytest.fixture(scope="session")
def client() -> str:
    login = uuid.uuid4().hex.upper()[0:8]

    return login


def pytest_configure():
    pytest.csrf_token = ''


@pytest.fixture()
def request_parser() -> RequestParser:
    scope = {
        "method": "GET",
        "path": "/task_list",
        "headers": [(b"authorization", b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                       b"eyJ1c2VySWQiOjJ9.evOVkQYocaFX3lwMBPwRmx8a4nvdNztHwIF1ajPfwqI")]
    }
    body = {}
    request_parser: RequestParser = RequestParser(body, scope['method'], scope['path'], scope['headers'])
    return request_parser


def test_method_now_allowed(request_parser: RequestParser) -> None:
    request_parser.method = 'SOME_METHOD'
    resp: Response = request_parser.parse()
    assert resp.status_code == 404


def test_options(request_parser: RequestParser) -> None:
    request_parser.method = 'OPTIONS'
    resp: Response = request_parser.parse()
    assert resp.status_code == 204


def test_reg(request_parser: RequestParser, client) -> None:
    request_parser.method = 'POST'
    request_parser.path = '/auth/reg'
    request_parser.body = {
        "username": client,
        "password": "1234"
    }
    resp: Response = request_parser.parse()

    assert resp.status_code == 200


def test_login(request_parser: RequestParser, client) -> None:
    request_parser.method = 'POST'
    request_parser.path = '/auth/login'
    request_parser.body = {
        "username": client,
        "password": "1234"
    }
    resp: Response = request_parser.parse()

    assert resp.status_code == 200


def test_get_task_lists(request_parser: RequestParser, client) -> None:
    request_parser.method = 'GET'
    resp: Response = request_parser.parse()
    pytest.csrf_token = json.loads(resp.body)[1]

    assert resp.status_code == 200


def test_get_task_lists_without_jwt(request_parser: RequestParser, client) -> None:
    request_parser.headers['authorization'] = 'not-a-jwt'
    resp: Response = request_parser.parse()

    assert resp.status_code == 401


def test_get_task_lists_admin(request_parser: RequestParser) -> None:
    request_parser.headers['authorization'] = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                                               'eyJ1c2VySWQiOjF9.5V-R2V8nUkCttP2o7OzyNql_UII1p1JNnK4Zd-ZKWt8')
    resp: Response = request_parser.parse()

    assert resp.status_code == 200


def test_create_task_list(request_parser: RequestParser, client) -> None:
    request_parser.method = 'POST'
    request_parser.body = {
        "task_list_name": client[:5],
    }
    request_parser.headers['x-csrf-token'] = pytest.csrf_token
    resp: Response = request_parser.parse()

    assert resp.status_code == 200


def test_task_list_exists(request_parser: RequestParser, client) -> None:
    request_parser.method = 'POST'
    request_parser.body = {
        "task_list_name": client[:5],
    }
    request_parser.headers['x-csrf-token'] = pytest.csrf_token
    resp: Response = request_parser.parse()

    assert resp.status_code == 400


def test_update_task_list(request_parser: RequestParser, client) -> None:
    request_parser.method = 'PUT'
    request_parser.body = {
        "task_list_old_name": client[:5],
        "task_list_new_name": "testing purpose"
    }
    resp: Response = request_parser.parse()

    assert resp.status_code == 200


def test_task_list_doesnt_exist(request_parser: RequestParser, client) -> None:
    request_parser.method = 'PUT'
    request_parser.body = {
        "task_list_old_name": "non existing task list",
        "task_list_new_name": "testing purpose"
    }
    resp: Response = request_parser.parse()

    assert resp.status_code == 400


def test_create_task(request_parser: RequestParser, client) -> None:
    request_parser.path = '/task'
    request_parser.method = 'POST'
    request_parser.body = {
        "task_list_name": "testing purpose",
        "task_name": client[:5]+'abc',
        "description": "for the testing purpose only"
    }
    request_parser.headers['x-csrf-token'] = pytest.csrf_token
    resp: Response = request_parser.parse()

    assert resp.status_code == 200


def test_get_task(request_parser: RequestParser, client) -> None:
    request_parser.path = '/task'
    request_parser.method = 'GET'
    request_parser.body = {
        "task_list_name": "testing purpose"
    }

    resp: Response = request_parser.parse()

    assert resp.status_code == 200


def test_get_task_admin(request_parser: RequestParser, client) -> None:
    request_parser.path = '/task'
    request_parser.headers['authorization'] = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjF9.'
                                               '5V-R2V8nUkCttP2o7OzyNql_UII1p1JNnK4Zd-ZKWt8')
    request_parser.body = {
        "task_list_name": "testing purpose"
    }
    resp: Response = request_parser.parse()

    assert resp.status_code == 200


def test_update_task(request_parser: RequestParser, client) -> None:
    request_parser.path = '/task'
    request_parser.method = 'PUT'
    request_parser.body = {
        "task_list_name": "testing purpose",
        "task_old_name": client[:5]+'abc',
        "task_new_name": client[:5] + 'new!!!',
        "new_desc": "for the testing purpose only"
    }
    resp: Response = request_parser.parse()

    assert resp.status_code == 200


def test_delete_task(request_parser: RequestParser, client) -> None:
    request_parser.path = '/task'
    request_parser.method = 'DELETE'
    request_parser.body = {
        "task_list_name": "testing purpose",
        "task_name": client[:5] + 'new!!!'
    }
    resp: Response = request_parser.parse()

    assert resp.status_code == 200


def test_delete_task_list(request_parser: RequestParser) -> None:
    request_parser.method = 'DELETE'
    request_parser.body = {
        "task_list_name": "testing purpose"
    }
    resp: Response = request_parser.parse()

    assert resp.status_code == 200


def test_task_list_doesnt_exist_del(request_parser: RequestParser) -> None:
    request_parser.method = 'DELETE'
    request_parser.body = {
        "task_list_name": "non existing task list"
    }
    resp: Response = request_parser.parse()

    assert resp.status_code == 400
