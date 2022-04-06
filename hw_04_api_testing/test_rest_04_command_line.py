import requests


def test_answer(url_given, status_given):
    r = requests.get(url_given)
    assert r.status_code == int(status_given)
