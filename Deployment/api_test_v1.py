# import packages
import pytest
from fastapi.testclient import TestClient
from api_v1 import app

client = TestClient(app)

# test to make sure api is functional
def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'API is functional.'}

# test prediction delay if there is no airport or it's invalid
def test_predict_no_airport():
    response = client.get('/predict/delays', params = {
        'arr_airport': 'LASTL',
        'dep_airport': 'LAX',
        'dep_time': '2025-01-10T09:00:00',
        'arr_time': '2025-01-10T17:00:00'
    })
    assert response.status_code == 404
    assert response.json() == {'detail': 'Arrival airport not found.'}