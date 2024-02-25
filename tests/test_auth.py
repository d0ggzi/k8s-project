import pytest

from src.web import auth, types, parser, tasks
import uuid


@pytest.fixture(scope="session")
def client():
    login = uuid.uuid4().hex.upper()[0:8]

    return login


def test_bad_reg():
    resp: types.Response = auth.register_user("", "")

    assert resp.status_code == 400
    assert resp.body == bytes("Username or password is required", encoding="raw_unicode_escape")


def test_user_reg(client):
    resp: types.Response = auth.register_user(client, "1234")

    assert resp.status_code == 200


def test_user_exists(client):
    resp: types.Response = auth.register_user(client, "1234")

    assert resp.status_code == 400
    assert resp.body == bytes("User with specified login already exists", encoding="raw_unicode_escape")


def test_bad_login():
    resp: types.Response = auth.login("", "")

    assert resp.status_code == 400
    assert resp.body == bytes("Username or password is required", encoding="raw_unicode_escape")


def test_invalid_cred():
    resp: types.Response = auth.login("maks", "1234")

    assert resp.status_code == 400
    assert resp.body == bytes("Invalid login or password", encoding="raw_unicode_escape")


def test_login(client):
    resp: types.Response = auth.login(client, "1234")
    print(resp.body)

    assert resp.status_code == 200
