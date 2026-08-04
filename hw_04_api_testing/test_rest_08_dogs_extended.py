import re

import pytest
import requests
from cerberus import Validator


BASE_URL = "https://dog.ceo/api"


def test_01_breed_list_has_expected_contract():
    schema = {
        "message": {
            "type": "dict",
            "valuesrules": {
                "type": "list",
                "schema": {"type": "string"},
            },
        },
        "status": {"type": "string", "allowed": ["success"]},
    }

    response = requests.get(f"{BASE_URL}/breeds/list/all", timeout=10)

    assert response.status_code == 200
    assert Validator(schema).validate(response.json())


def test_02_sub_breed_list_belongs_to_requested_breed():
    response = requests.get(f"{BASE_URL}/breed/hound/list", timeout=10)
    result = response.json()

    assert response.status_code == 200
    assert result["status"] == "success"
    assert result["message"] == ["afghan", "basset", "blood", "english", "ibizan", "walker"]


@pytest.mark.parametrize("breed", ["hound", "akita"])
def test_03_breed_images_are_hosted_by_dog_ceo(breed):
    response = requests.get(f"{BASE_URL}/breed/{breed}/images", timeout=10)
    result = response.json()

    assert response.status_code == 200
    assert result["status"] == "success"
    assert result["message"]

    image_pattern = re.compile(rf"^https://images\.dog\.ceo/breeds/{breed}(?:-|/).+")
    assert all(image_pattern.match(image) for image in result["message"])


def test_04_random_image_response_contains_valid_image_url():
    response = requests.get(f"{BASE_URL}/breeds/image/random", timeout=10)
    result = response.json()

    assert response.status_code == 200
    assert result["status"] == "success"
    assert re.match(r"^https://images\.dog\.ceo/breeds/.+\.(?:jpg|jpeg|png)$", result["message"])


def test_05_random_images_count_is_limited_to_fifty():
    response = requests.get(f"{BASE_URL}/breeds/image/random/100", timeout=10)
    result = response.json()

    assert response.status_code == 200
    assert result["status"] == "success"
    assert len(result["message"]) == 50


def test_06_unknown_breed_returns_error_contract():
    response = requests.get(f"{BASE_URL}/breed/not-a-real-breed/images", timeout=10)
    result = response.json()

    assert response.status_code == 404
    assert result["status"] == "error"
    assert result["message"] == "Breed not found (master breed does not exist)"
