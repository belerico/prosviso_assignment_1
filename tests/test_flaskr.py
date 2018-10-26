from flaskr import flaskr
import pytest


@pytest.fixture
def client():
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()
    yield client

def test_empty_db(client):
    """Start with a blank database."""

    r = client.get('http://api:7000/api/users/count').json()
    assert 0 in r["count"]