import requests
import pytest

BASE_URL = "http://localhost:3000/BookLibrary"
BOOK_ID = "abc1234"
BOOK_URL = f"{BASE_URL}/{BOOK_ID}"

payload = {
    "id": BOOK_ID,
    "name": "SDET - Python",
    "isbn": "opq",
    "aisle": "444",
    "author": "Jyoti"
}

@pytest.fixture
def initial_state():
    """Get the state before test run"""
    response = requests.get(BASE_URL)
    response.raise_for_status()
    return response.json()

def test_integration(initial_state):
    # 1. POST → Add new book
    post_response = requests.post(BASE_URL, json=payload)
    assert post_response.status_code == 201, "POST request should always return 201"
    assert post_response.json()["id"] == BOOK_ID  # match created book id

    # 2. DELETE → Remove the same book
    delete_response = requests.delete(BOOK_URL)
    assert delete_response.status_code == 200, "DELETE request should always return 200"

    # 3. GET again → Should match initial state
    final_response = requests.get(BASE_URL)
    assert final_response.status_code == 200
    assert final_response.json() == initial_state, "Final GET should match initial GET"
