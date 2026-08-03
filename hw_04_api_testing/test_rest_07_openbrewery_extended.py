import pytest
import requests

pytestmark = pytest.mark.usefixtures("log_test_case")

BASE_URL = "https://api.openbrewerydb.org/v1/breweries"


@pytest.mark.parametrize("per_page", [1, 5, 10])
def test_01_per_page_limits_results(per_page):
    r = requests.get(f"{BASE_URL}?per_page={per_page}", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert len(result) == per_page


def test_02_pagination_returns_different_pages():
    r1 = requests.get(f"{BASE_URL}?per_page=5&page=1", timeout=10)
    r2 = requests.get(f"{BASE_URL}?per_page=5&page=2", timeout=10)

    assert r1.status_code == 200
    assert r2.status_code == 200

    ids_page_1 = {b["id"] for b in r1.json()}
    ids_page_2 = {b["id"] for b in r2.json()}
    assert ids_page_1.isdisjoint(ids_page_2)


def test_03_metadata_total_is_positive():
    r = requests.get(f"{BASE_URL}/meta", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert int(result["total"]) > 0


@pytest.mark.parametrize(
    "brewery_type",
    ["micro", "nano", "brewpub", "large"],
)
def test_04_filter_by_type(brewery_type):
    r = requests.get(f"{BASE_URL}?by_type={brewery_type}&per_page=10", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert len(result) > 0
    for brewery in result:
        assert brewery["brewery_type"] == brewery_type


def test_05_search_endpoint_matches_query():
    r = requests.get(f"{BASE_URL}/search?query=dog&per_page=5", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert len(result) > 0
    for brewery in result:
        assert "dog" in brewery["name"].lower()


def test_06_single_random_brewery():
    r = requests.get(f"{BASE_URL}/random", timeout=10)
    result = r.json()

    assert r.status_code == 200
    assert len(result) == 1
    assert "id" in result[0]
    assert "name" in result[0]
