import pytest

# ---------------------
# INDEX PAGE REQUESTS
# ---------------------
def test_getIndex(test_client, data):
    """
    Index Page GET Request
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'OurOrder' in response.data
    assert b'Enter Your Order' in response.data    

def test_postSuccessIndex(test_client, data):
    """
    Index Page POST Request SUCCESS
    """
    info = {
        'name': 'John',
        'order': 'Ribeye Steak',
        'session': 11111,
        'price': 12.00,
        'notes': 'With extra sauce'
    }
    response = test_client.post('/', data=info, follow_redirects=True)
    assert response.status_code == 200
    assert b'OurOrder' in response.data
    assert b'Enter Your Order' in response.data  

def test_postFailIndex(test_client, data):
    """
    Index Page POST Request FAIL
    """
    info = {
        'name': "",
        'order': "",
        'session': "",
        'price': 12.00,
        'notes': 'With extra sauce'
    }
    response = test_client.post('/', data=info, follow_redirects=True)
    assert response.status_code == 200
    assert b'OurOrder' in response.data
    assert b'Enter Your Order' in response.data 
    assert b'Name is required' in response.data 
    assert b'Session is required' in response.data 
    assert b'Order is required' in response.data 
    assert b'5 digits' in response.data 


# ---------------------
# ORDER PAGE REQUESTS
# ---------------------
def test_getOrders(test_client, data):
    """
    Orders Page GET Request
    """
    response = test_client.get('/orders')
    assert response.status_code == 200
    assert b'OurOrder' in response.data
    assert b'Check' in response.data    
    assert b'Session ID' in response.data

def test_postNoOrders(test_client, data):
    """
    Orders Page POST Request NO Order
    """
    info = {
        'session': 11112,
    }
    response = test_client.post('/orders', data=info, follow_redirects=True)
    assert response.status_code == 200
    assert b'OurOrder' in response.data
    assert b'Check' in response.data    
    assert b'Session ID' in response.data
    assert b'not currently in use' in response.data

def test_postSuccessOrders(test_client, data):
    """
    Orders Page POST Request SUCCESS
    """
    info = {
        'session': 11111,
    }
    response = test_client.post('/orders', data=info, follow_redirects=True)
    assert response.status_code == 200
    assert b'OurOrder' in response.data
    assert b'Check' in response.data    
    assert b'Session ID' in response.data
    assert b'Total bill' in response.data

def test_postFailOrders(test_client, data):
    """
    Orders Page POST Request FAIL
    """
    info = {
        'session': "",
    }
    response = test_client.post('/orders', data=info, follow_redirects=True)
    assert response.status_code == 200
    assert b'OurOrder' in response.data
    assert b'Check' in response.data    
    assert b'Session ID is required and must be 5 digits!' in response.data

# ---------------------
# GENERATE PAGE REQUESTS
# ---------------------
def test_getGenerate(test_client, data):
    """
    Generate Page GET Request
    """
    response = test_client.get('/generate', follow_redirects=True)
    assert response.status_code == 200
    assert b'OurOrder' in response.data
    assert b'Check' in response.data    
    assert b'Session ID' in response.data     

# ---------------------
# EXPORT PAGE REQUESTS
# ---------------------
def test_postExport(test_client, data):
    """
    Export Page GET Request
    """
    orders = {
        "orders":{"YT": ["Potato Salad", "With extra cream", "3.00"], "Keith": ["Potato Soup", "With extra eggs", "10.00"], "John": ["Ribeye Steak", "With extra sauce", "12.00"], "Alex": ["Mcchicken meal with potato pie", "Upsize, drink coke no ice", "20.00"]}
    }   
    response = test_client.post('/export', json=orders, content_type='application/json', follow_redirects=True)
    assert response.status_code == 200
    assert b'xml' in response.data