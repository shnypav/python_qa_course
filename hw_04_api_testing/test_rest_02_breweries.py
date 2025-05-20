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
