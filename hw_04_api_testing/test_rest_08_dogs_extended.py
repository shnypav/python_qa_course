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


@pytest.mark.parametrize("breed, sub_breed", [("hound", "afghan"), ("poodle", "toy")])
def test_07_sub_breed_images_belong_to_requested_sub_breed(breed, sub_breed):
    response = requests.get(f"{BASE_URL}/breed/{breed}/{sub_breed}/images", timeout=10)
    result = response.json()

    assert response.status_code == 200
    assert result["status"] == "success"
    assert result["message"]

    prefix = f"https://images.dog.ceo/breeds/{breed}-{sub_breed}/"
    assert all(image.startswith(prefix) for image in result["message"])


@pytest.mark.parametrize("count", [1, 5], ids=["single image", "several images"])
def test_08_random_breed_images_return_requested_count_of_that_breed(count):
    response = requests.get(f"{BASE_URL}/breed/akita/images/random/{count}", timeout=10)
    result = response.json()

    assert response.status_code == 200
    assert result["status"] == "success"
    assert len(result["message"]) == count
    assert all(image.startswith("https://images.dog.ceo/breeds/akita/") for image in result["message"])


def test_09_unknown_sub_breed_returns_error_contract():
    response = requests.get(f"{BASE_URL}/breed/hound/not-a-real-sub-breed/images", timeout=10)
    result = response.json()

    assert response.status_code == 404
    assert result["status"] == "error"
    assert "not found" in result["message"].lower()


def test_10_sub_breed_endpoint_matches_full_breed_list():
    all_breeds = requests.get(f"{BASE_URL}/breeds/list/all", timeout=10).json()["message"]
    breeds_with_sub_breeds = sorted(breed for breed, sub_breeds in all_breeds.items() if sub_breeds)[:3]

    assert breeds_with_sub_breeds

    for breed in breeds_with_sub_breeds:
        response = requests.get(f"{BASE_URL}/breed/{breed}/list", timeout=10)
        result = response.json()

        assert response.status_code == 200
        assert result["status"] == "success"
        assert sorted(result["message"]) == sorted(all_breeds[breed])


def test_11_breed_names_are_lowercase_single_words():
    response = requests.get(f"{BASE_URL}/breeds/list/all", timeout=10)
    all_breeds = response.json()["message"]

    assert response.status_code == 200
    assert {"hound", "poodle", "terrier"} <= set(all_breeds)

    names = list(all_breeds) + [sub for sub_breeds in all_breeds.values() for sub in sub_breeds]
    assert all(re.fullmatch(r"[a-z]+", name) for name in names)


def test_12_random_image_url_points_to_a_downloadable_image():
    image_url = requests.get(f"{BASE_URL}/breeds/image/random", timeout=10).json()["message"]

    image_response = requests.head(image_url, allow_redirects=True, timeout=10)

    assert image_response.status_code == 200
    assert image_response.headers["Content-Type"].startswith("image/")


@pytest.mark.parametrize("endpoint", ["breeds/list/all", "breeds/image/random", "breed/hound/list"])
def test_13_responses_are_served_as_json(endpoint):
    response = requests.get(f"{BASE_URL}/{endpoint}", timeout=10)

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
