import pytest
import requests
from cerberus import Validator

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_01_put_replaces_post():
    payload = {"id": 1, "title": "Replaced title", "body": "Replaced body", "userId": 1}
    r = requests.put(f"{BASE_URL}/posts/1", json=payload, timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert result["title"] == "Replaced title"
    assert result["body"] == "Replaced body"


def test_02_post_schema():
    schema = {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    }
    v = Validator(schema, require_all=True)

    r = requests.get(f"{BASE_URL}/posts/1", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert v.validate(result), v.errors


@pytest.mark.parametrize(
    "resource, expected_qty",
    [("posts", 100), ("comments", 500), ("albums", 100), ("todos", 200), ("users", 10)],
    ids=["posts", "comments", "albums", "todos", "users"],
)
def test_03_resource_collection_size(resource, expected_qty):
    r = requests.get(f"{BASE_URL}/{resource}", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert len(result) == expected_qty


@pytest.mark.parametrize("user_id", [1, 5, 10])
def test_04_user_albums_belong_to_user(user_id):
    r = requests.get(f"{BASE_URL}/users/{user_id}/albums", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert len(result) > 0
    for album in result:
        assert album["userId"] == user_id


def test_05_completed_todos_filter():
    r = requests.get(f"{BASE_URL}/todos?completed=true", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert len(result) > 0
    for todo in result:
        assert todo["completed"] is True


def test_06_user_schema():
    schema = {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string"},
        "address": {
            "type": "dict",
            "schema": {
                "street": {"type": "string"},
                "city": {"type": "string"},
                "zipcode": {"type": "string"},
                "geo": {
                    "type": "dict",
                    "schema": {"lat": {"type": "string"}, "lng": {"type": "string"}},
                },
            },
        },
    }
    v = Validator(schema, allow_unknown=True)

    r = requests.get(f"{BASE_URL}/users/1", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert v.validate(result), v.errors
