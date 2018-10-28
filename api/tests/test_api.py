import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "api"))
from api import api

@pytest.fixture
def client():
    api.app.config["TESTING"] = True
    client = api.app.test_client()
    yield client

def test_add_user(client):
    r = client.get('/api/users/count').get_json()
    count = r["count"]
    client.post('/api/user/a')
    r = client.get('/api/users/count').get_json()
    new_count = r["count"]
    assert new_count == count or new_count == count + 1

def test_delete_all_users(client):
    assert client.delete('/api/users').status_code == 200
    r = client.get('/api/users/count').get_json()
    assert r["count"] == 0

def test_sort_users(client):
    client.post('/api/user/b')
    client.post('/api/user/b')
    client.post('/api/user/a')
    r = client.get('/api/users/sort/desc').get_json()
    exp = [{"count":"2","username":"b"},{"count":"1","username":"a"}]
    assert r == exp

def test_sort_users_break(client):
    client.post('/api/user/a')
    r = client.get('/api/users/sort/desc').get_json()
    exp = [{"count":"2","username":"a"},{"count":"2","username":"b"}]
    assert r == exp

def test_max(client):
    r = client.get('/api/users/max').get_json()
    for x in r:
        assert x["count"] == "2"
