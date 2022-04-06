import pytest
import requests
from cerberus import Validator


@pytest.mark.parametrize("url", ["https://dog.ceo/api/breeds/list/all",
                                 "https://dog.ceo/api/breeds/image/random",
                                 "https://dog.ceo/api/breed/hound/images",
                                 "https://dog.ceo/api/breed/hound/list"])
def test_01_response_200(url):
    r = requests.get(url)
    assert r.status_code == 200


@pytest.mark.parametrize("url, message_type", [("https://dog.ceo/api/breeds/list/all", "dict"),
                                               ("https://dog.ceo/api/breeds/image/random", "string")])
def test_02_schemas(url, message_type):
    schema = {
        "message": {
            "type": message_type
        },
        "status": {
            "type": "string"
        }
    }
    v = Validator(schema)

    r = requests.get(url)
    assert r.status_code == 200
    assert v.validate(r.json(), schema)


@pytest.mark.parametrize("num, exp",
                         [(3, 3), (0, 1), (50, 50), (51, 50), (-1, 1)],
                         ids=["Normal case", "Zero case", "Max value", "More than max value", "Negative value"])
def test_03_multiple_random(num, exp):
    r = requests.get(f"https://dog.ceo/api/breeds/image/random/{num}")
    result = r.json()
    assert r.status_code == 200
    assert len(result["message"]) == exp


# https://dog.ceo/api/breed/akita/images/random
# the result link contains name of the breed requested, e.g.
# "message": "https://images.dog.ceo/breeds/hound-afghan/n02088094_7636.jpg",
@pytest.mark.parametrize("breed", ["hound", "akita", "collie"])
def test_04_random_image_for_breed(breed):
    r = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
    result = r.json()
    assert r.status_code == 200
    assert breed in result["message"]


# https://dog.ceo/api/breed/hound/afghan/images
# to check if all images for sub-breed are for exact breed and sub-breed
# "https://images.dog.ceo/breeds/hound-afghan/n02088094_10263.jpg",
@pytest.mark.parametrize("breed, sub_breed", [("hound", "afghan"), ("poodle", "toy")])
def test_05_sub_breed_images(breed, sub_breed):
    r = requests.get(f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images")
    result = r.json()
    assert r.status_code == 200
    for image in result["message"]:
        assert f"{breed}-{sub_breed}" in image
