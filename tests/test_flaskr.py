import pytest
import sys

sys.path.insert(0, '/api/api.py')
import flaskAPI

@pytest.fixture
def client():
    flaskAPI.app.config['TESTING'] = True
    client = flaskAPI.app.test_client()
    yield client

def test_empty_db(client):
    """Start with a blank database."""

    r = client.get('http://api:7000/api/users/count').json()
    assert 0 in r["count"]