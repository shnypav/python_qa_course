import pytest
import requests


def test_dog_api_unknown_breed_returns_error():
    r = requests.get("https://dog.ceo/api/breed/not-a-real-breed/images/random", timeout=10)
    result = r.json()

    assert r.status_code == 404
    assert result["status"] == "error"
    assert "Breed not found" in result["message"]


def test_dog_api_breed_list_contains_expected_sub_breed():
    r = requests.get("https://dog.ceo/api/breeds/list/all", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert result["status"] == "success"
    assert "hound" in result["message"]
    assert "afghan" in result["message"]["hound"]


def test_open_brewery_response_contains_required_fields():
    required_fields = {"id", "name", "brewery_type", "city", "state", "country"}

    r = requests.get("https://api.openbrewerydb.org/v1/breweries?by_city=oakland&per_page=3", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert len(result) > 0
    for brewery in result:
        assert required_fields.issubset(brewery.keys())
        assert brewery["city"].lower() == "oakland"


def test_open_brewery_unknown_id_returns_not_found():
    r = requests.get("https://api.openbrewerydb.org/v1/breweries/not-a-real-id", timeout=10)

    assert r.status_code == 404
    assert "Not Found" in r.text


def test_jsonplaceholder_unknown_post_returns_empty_object():
    r = requests.get("https://jsonplaceholder.typicode.com/posts/999999", timeout=10)

    assert r.status_code == 404
    assert r.json() == {}


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "Updated title"},
        {"body": "Updated body"},
    ],
)
def test_jsonplaceholder_patch_post_returns_updated_fields(payload):
    r = requests.patch("https://jsonplaceholder.typicode.com/posts/1", json=payload, timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert result["id"] == 1
    for field, value in payload.items():
        assert result[field] == value
