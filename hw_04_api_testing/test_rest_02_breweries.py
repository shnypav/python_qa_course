import pytest
import requests

@pytest.mark.parametrize("field, search_string",
                         [("city", "oakland"), ("name", "crown")])
def test_01_brewery_by_field(field, search_string):
    r = requests.get(f"https://api.openbrewerydb.org/v1/breweries?by_{field}={search_string}")
    result = r.json()
    assert r.status_code == 200
    assert len(result) > 0
    if field == "city":
        for brewery in result:
            assert search_string.lower() in brewery["city"].lower()
    elif field == "name":
        for brewery in result:
            assert search_string.lower() in brewery["name"].lower()

def test_02_brewery_by_type():
    r = requests.get("https://api.openbrewerydb.org/v1/breweries?by_type=micro")
    result = r.json()
    assert r.status_code == 200
    assert len(result) > 0
    for brewery in result:
        assert brewery["brewery_type"] == "micro"

def test_03_brewery_by_id():
    r = requests.get("https://api.openbrewerydb.org/v1/breweries?by_type=micro")
    result = r.json()
    assert r.status_code == 200
    assert len(result) > 0
    brewery_id = result[0]["id"]
    r = requests.get(f"https://api.openbrewerydb.org/v1/breweries/{brewery_id}")
    result = r.json()
    assert r.status_code == 200
    assert result["id"] == brewery_id


@pytest.mark.parametrize("per_page", [3, 5, 10])
def test_04_brewery_pagination_per_page(per_page):
    r = requests.get(f"https://api.openbrewerydb.org/v1/breweries?per_page={per_page}")
    result = r.json()
    assert r.status_code == 200
    assert len(result) == per_page


def test_05_brewery_pagination_pages_differ():
    r1 = requests.get("https://api.openbrewerydb.org/v1/breweries?per_page=5&page=1")
    r2 = requests.get("https://api.openbrewerydb.org/v1/breweries?per_page=5&page=2")
    assert r1.status_code == 200
    assert r2.status_code == 200
    ids_page1 = {b["id"] for b in r1.json()}
    ids_page2 = {b["id"] for b in r2.json()}
    assert ids_page1.isdisjoint(ids_page2)


def test_06_brewery_search():
    search_term = "dog"
    r = requests.get(f"https://api.openbrewerydb.org/v1/breweries?by_search={search_term}")
    result = r.json()
    assert r.status_code == 200
    assert len(result) > 0
    for brewery in result:
        name_or_city = brewery.get("name", "") + brewery.get("city", "")
        assert search_term.lower() in name_or_city.lower()


@pytest.mark.parametrize("brewery_type", ["micro", "nano", "regional", "brewpub", "large"])
def test_07_valid_brewery_types(brewery_type):
    r = requests.get(f"https://api.openbrewerydb.org/v1/breweries?by_type={brewery_type}&per_page=3")
    result = r.json()
    assert r.status_code == 200
    for brewery in result:
        assert brewery["brewery_type"] == brewery_type
