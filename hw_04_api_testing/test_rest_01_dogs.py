import logging

import pytest
import requests
from cerberus import Validator


logger = logging.getLogger(__name__)


def get_dog_api(url):
    logger.info("GET %s", url)
    response = requests.get(url, timeout=10)
    logger.info("Response status: %s", response.status_code)
    return response


@pytest.mark.parametrize("url", ["https://dog.ceo/api/breeds/list/all",
                                 "https://dog.ceo/api/breeds/image/random",
                                 "https://dog.ceo/api/breed/hound/images",
                                 "https://dog.ceo/api/breed/hound/list"])
def test_01_response_200(url):
    r = get_dog_api(url)
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

    r = get_dog_api(url)
    result = r.json()
    is_valid = v.validate(result, schema)
    logger.info("Schema validation for %s expected message type %s: %s", url, message_type, is_valid)

    assert r.status_code == 200
    assert is_valid


@pytest.mark.parametrize("num, exp",
                         [(3, 3), (0, 1), (50, 50), (51, 50), (-1, 1)],
                         ids=["Normal case", "Zero case", "Max value", "More than max value", "Negative value"])
def test_03_multiple_random(num, exp):
    r = get_dog_api(f"https://dog.ceo/api/breeds/image/random/{num}")
    result = r.json()
    logger.info("Requested %s images, expected %s, received %s", num, exp, len(result["message"]))

    assert r.status_code == 200
    assert len(result["message"]) == exp


# https://dog.ceo/api/breed/akita/images/random
# the result link contains name of the breed requested, e.g.
# "message": "https://images.dog.ceo/breeds/hound-afghan/n02088094_7636.jpg",
@pytest.mark.parametrize("breed", ["hound", "akita", "collie"])
def test_04_random_image_for_breed(breed):
    r = get_dog_api(f"https://dog.ceo/api/breed/{breed}/images/random")
    result = r.json()
    logger.info("Breed %s random image: %s", breed, result["message"])

    assert r.status_code == 200
    assert breed in result["message"]


# https://dog.ceo/api/breed/hound/afghan/images
# to check if all images for sub-breed are for exact breed and sub-breed
# "https://images.dog.ceo/breeds/hound-afghan/n02088094_10263.jpg",
@pytest.mark.parametrize("breed, sub_breed", [("hound", "afghan"), ("poodle", "toy")])
def test_05_sub_breed_images(breed, sub_breed):
    r = get_dog_api(f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images")
    result = r.json()
    logger.info("Breed %s sub-breed %s returned %s images", breed, sub_breed, len(result["message"]))

    assert r.status_code == 200
    for image in result["message"]:
        assert f"{breed}-{sub_breed}" in image
