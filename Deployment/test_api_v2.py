# import packages
import pytest
from fastapi.testclient import TestClient
from api_v2 import app

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

# test prediction delay when the time is correctly formatted
def test_predict_correct_format():
    response = client.get('/predict/delays', params = {
        'arr_airport': 'JFK',
        'dep_airport': 'LAX',
        'dep_time': '2025-01-10T09:00:00',
        'arr_time': '2025-01-10T17:00:00'
    })
    assert response.status_code == 200
    assert 'Average Departure Delay' in response.json()

# test prediction delay when the time is incorrectly formatted
def test_predict_incorrect_format():
    response = client.get('/predict/delays', params = {
        'arr_airport': 'JFK',
        'dep_airport': 'LAX',
        'dep_time': '01-10-2025T09:00:00',
        'arr_time': '2025-01-10T17:00:00'
    })
    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid time format. Time must be "YYYY-MM-DDTHH:MM:SS".'}

# test prediction delay when the departure is in the future
def test_predict_delays_future_date():
    response = client.get("/predict/delays", params={
        "arr_airport": "JFK",
        "dep_airport": "LAX",
        "dep_time": "2050-01-10T09:00:00",
        "arr_time": "2050-01-10T17:00:00"
    })
    assert response.status_code == 200
    assert "Average Departure Delay" in response.json()