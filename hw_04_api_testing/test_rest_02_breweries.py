import pytest
import requests


# test 1
# https://api.openbrewerydb.org/breweries
# filter breweries by something
@pytest.mark.parametrize("field, search_string",
                         [("city", "oakland"), ("name", "crown")])
def test_01_brewery_by_field(field, search_string):
    r = requests.get(f"https://api.openbrewerydb.org/breweries?by_{field}={search_string}")
    result = r.json()
    assert r.status_code == 200
    for brewery in result:
        assert search_string in str(brewery[field]).lower()


# test 2
# https://api.openbrewerydb.org/breweries/madtree-brewing-cincinnati
# get brewery by post_id, post_id should be = search string
@pytest.mark.parametrize("id", ["08f78223-24f8-4b71-b381-ea19a5bd82df", "fb94830f-6196-4f59-9189-c9060b778085"])
def test_02_brewery_by_id(id):
    r = requests.get(f"https://api.openbrewerydb.org/breweries/{id}")
    result = r.json()
    assert r.status_code == 200
    assert result["id"] == id


# test 3
# https://api.openbrewerydb.org/breweries/search?query=dog
# check using "_" and "%20" as space in search
@pytest.mark.parametrize("name_send, name_receive",
                         [("Running_Dogs_Brewery", "Running Dogs Brewery"),
                          ("Bike%20Dog%20Brewing%20Co", "Bike Dog Brewing Co")],
                         ids=["Space as underscore", "Space as %20"])
def test_03_space_in_name(name_send, name_receive):
    r = requests.get(f"https://api.openbrewerydb.org/breweries/search?query={name_send}")
    result = r.json()

    assert r.status_code == 200
    assert result[0]["name"] == name_receive


# test 4
# https://api.openbrewerydb.org/breweries/search?query=dog
# name of each element contains search string
def test_04_search_name():
    name = "crown"
    r = requests.get(f"https://api.openbrewerydb.org/breweries/search?query={name}")
    result = r.json()
    assert r.status_code == 200
    assert name in str(result[0]["name"]).lower()


# test 5
# https://api.openbrewerydb.org/breweries/autocomplete?query=dog
# schema post_id, name and name contains string from query
# max number = 15
@pytest.mark.xfail
def test_05_autocomplete():
    name = "dog"
    r = requests.get(f"https://api.openbrewerydb.org/breweries/autocomplete?query={name}")
    result = r.json()
    assert r.status_code == 200
    for brewery in result:
        assert name in str(brewery["name"]).lower()
    # next assertion will fail but per documentation, max results = 15
    # https://www.openbrewerydb.org/documentation/04-autocomplete
    assert len(result) == 15
