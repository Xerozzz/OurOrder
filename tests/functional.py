import pytest

# GET REQUESTS
def test_getIndex(test_client, data):
    """
    Index Page GET Request
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'OurOrder' in response.data
    assert b'Enter Your Order' in response.data    

def test_getOrders(test_client, data):
    """
    Orders Page GET Request
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'OurOrder' in response.data
    assert b'Check' in response.data    
    assert b'Session ID' in response.data    

def test_getGenerate(test_client, data):
    """
    Generate Page GET Request
    """
    response = test_client.get('/')
    assert response.status_code == 200