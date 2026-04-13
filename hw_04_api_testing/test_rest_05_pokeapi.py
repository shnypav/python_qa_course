import pytest
import requests

BASE_URL = "https://pokeapi.co/api/v2"


@pytest.mark.parametrize("name, expected_id", [
    ("pikachu", 25),
    ("bulbasaur", 1),
    ("charmander", 4),
])
def test_01_get_pokemon_by_name(name, expected_id):
    r = requests.get(f"{BASE_URL}/pokemon/{name}")
    result = r.json()
    assert r.status_code == 200
    assert result["name"] == name
    assert result["id"] == expected_id


@pytest.mark.parametrize("pokemon_id, expected_name", [
    (1, "bulbasaur"),
    (25, "pikachu"),
    (150, "mewtwo"),
])
def test_02_get_pokemon_by_id(pokemon_id, expected_name):
    r = requests.get(f"{BASE_URL}/pokemon/{pokemon_id}")
    result = r.json()
    assert r.status_code == 200
    assert result["id"] == pokemon_id
    assert result["name"] == expected_name


def test_03_pokemon_list_pagination():
    r1 = requests.get(f"{BASE_URL}/pokemon?limit=5&offset=0")
    r2 = requests.get(f"{BASE_URL}/pokemon?limit=5&offset=5")
    assert r1.status_code == 200
    assert r2.status_code == 200
    names_page1 = {p["name"] for p in r1.json()["results"]}
    names_page2 = {p["name"] for p in r2.json()["results"]}
    assert len(names_page1) == 5
    assert len(names_page2) == 5
    assert names_page1.isdisjoint(names_page2)


@pytest.mark.parametrize("pokemon_name, expected_type", [
    ("pikachu", "electric"),
    ("charmander", "fire"),
    ("squirtle", "water"),
    ("bulbasaur", "grass"),
])
def test_04_pokemon_primary_type(pokemon_name, expected_type):
    r = requests.get(f"{BASE_URL}/pokemon/{pokemon_name}")
    result = r.json()
    assert r.status_code == 200
    types = [t["type"]["name"] for t in result["types"]]
    assert expected_type in types


def test_05_invalid_pokemon_returns_404():
    r = requests.get(f"{BASE_URL}/pokemon/notapokemon12345")
    assert r.status_code == 404


@pytest.mark.parametrize("pokemon_name", ["pikachu", "mewtwo", "eevee"])
def test_06_pokemon_has_required_fields(pokemon_name):
    r = requests.get(f"{BASE_URL}/pokemon/{pokemon_name}")
    result = r.json()
    assert r.status_code == 200
    for field in ["id", "name", "base_experience", "height", "weight", "abilities", "types", "stats"]:
        assert field in result


@pytest.mark.parametrize("type_name", ["fire", "water", "grass", "electric"])
def test_07_type_has_pokemon(type_name):
    r = requests.get(f"{BASE_URL}/type/{type_name}")
    result = r.json()
    assert r.status_code == 200
    assert result["name"] == type_name
    assert len(result["pokemon"]) > 0


def test_08_pokemon_count_in_list():
    r = requests.get(f"{BASE_URL}/pokemon?limit=1")
    result = r.json()
    assert r.status_code == 200
    assert result["count"] > 1000
