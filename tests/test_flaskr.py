import pytest
import requests

def test_empty_db():
    """Start with a blank database."""
    
    r = requests.get('http://api:7000/api/users/count').json()
    assert 0 == r["count"]