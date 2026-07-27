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


# https://dog.ceo/api/breed/hound/list
# the sub-breeds reported for one breed must match what /breeds/list/all reports for it
# affenpinscher is the edge case: a breed with no sub-breeds at all -> []
@pytest.mark.parametrize("breed", ["hound", "bulldog", "affenpinscher"])
def test_06_sub_breed_list_matches_full_list(breed):
    all_breeds = requests.get("https://dog.ceo/api/breeds/list/all", timeout=10).json()

    r = requests.get(f"https://dog.ceo/api/breed/{breed}/list", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert result["status"] == "success"
    assert sorted(result["message"]) == sorted(all_breeds["message"][breed])


# https://dog.ceo/api/breed/hound/images/random/3
# several random images at once, but restricted to a single breed
@pytest.mark.parametrize("num", [1, 3, 10])
def test_07_multiple_random_images_for_breed(num):
    breed = "hound"

    r = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random/{num}", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert len(result["message"]) == num
    for image in result["message"]:
        assert breed in image


# https://dog.ceo/api/breed/hound/afghan/images/random
@pytest.mark.parametrize("breed, sub_breed", [("hound", "afghan"), ("bulldog", "french"), ("poodle", "toy")])
def test_08_random_sub_breed_image(breed, sub_breed):
    r = requests.get(f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert result["status"] == "success"
    assert f"{breed}-{sub_breed}" in result["message"]


# https://dog.ceo/api/breed/hound/images/alt
# the /alt endpoints return image urls together with their alt text
def test_09_alt_endpoint_schema():
    schema = {
        "message": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "url": {"type": "string", "required": True},
                    "alt": {"type": "string", "required": True}
                }
            }
        },
        "status": {
            "type": "string",
            "allowed": ["success"]
        }
    }
    v = Validator(schema)

    r = requests.get("https://dog.ceo/api/breed/hound/images/alt", timeout=10)

    assert r.status_code == 200
    assert v.validate(r.json(), schema), v.errors


# breed names are case-sensitive, only lowercase is accepted
@pytest.mark.parametrize("breed", ["Hound", "HOUND", "Akita"])
def test_10_breed_names_are_case_sensitive(breed):
    r = requests.get(f"https://dog.ceo/api/breed/{breed}/images", timeout=10)
    result = r.json()

    assert r.status_code == 404
    assert result["status"] == "error"


# an existing breed with a sub-breed that does not belong to it
@pytest.mark.parametrize("breed, sub_breed", [("hound", "toy"), ("hound", "not-a-real-sub-breed")])
def test_11_unknown_sub_breed_returns_error(breed, sub_breed):
    r = requests.get(f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images", timeout=10)
    result = r.json()

    assert r.status_code == 404
    assert result["status"] == "error"


# every value in /breeds/list/all must be a list of non-empty lowercase sub-breed names
def test_12_all_breeds_values_are_sub_breed_lists():
    r = requests.get("https://dog.ceo/api/breeds/list/all", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert result["status"] == "success"
    assert len(result["message"]) > 50

    for breed, sub_breeds in result["message"].items():
        assert breed == breed.lower()
        assert isinstance(sub_breeds, list)
        for sub_breed in sub_breeds:
            assert isinstance(sub_breed, str)
            assert sub_breed == sub_breed.lower()


# the url we get back must not only look like an image, it must actually serve one
def test_13_random_image_url_is_reachable():
    r = requests.get("https://dog.ceo/api/breeds/image/random", timeout=10)
    image_url = r.json()["message"]

    assert r.status_code == 200
    assert image_url.startswith("https://images.dog.ceo/breeds/")
    assert image_url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))

    image = requests.head(image_url, timeout=10, allow_redirects=True)

    assert image.status_code == 200
    assert image.headers["Content-Type"].startswith("image/")
