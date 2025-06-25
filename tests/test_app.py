import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_root(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Preisrechner' in resp.data

def test_valid_post(client):
    data = {
        'ek_netto': '100',
        'mwst': '19',
        'aufschlag': '10',
        'aufschlag_typ': '%'
    }
    resp = client.post('/', data=data)
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert '100.00 €' in html
    assert '119.00 €' in html
    assert '110.00 €' in html
    assert '130.90 €' in html
