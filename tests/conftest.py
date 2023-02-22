import pytest
from app import app

@pytest.fixture(scope="module")
def test_client():
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module")
def data():
    item = {
        "YT": ["Potato Salad", "With extra cream", "3.00"],
        "Keith": ["Potato Soup", "With extra eggs", "10.00"],      
        "John": ["Ribeye Steak", "With extra sauce", "12.00"],  
        "Alex": ["Mcchicken meal with potato pie", "Upsize, drink coke no ice", "20.00"],  
    }
    return item