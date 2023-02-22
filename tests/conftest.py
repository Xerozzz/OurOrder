import pytest
from ourorder import create_app

@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()
    testing_client = flask_app.test_client()
    with flask_app.app_context():
        yield testing_client

@pytest.fixture(scope="module")
def data():
    item = {
        "YT": ["Potato Salad", "With extra cream", "3.00"],
        "Keith": ["Potato Soup", "With extra eggs", "10.00"],      
        "John": ["Ribeye Steak", "With extra sauce", "12.00"],  
        "Alex": ["Mcchicken meal with potato pie", "Upsize, drink coke no ice", "20.00"],  
    }
    return item