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
    assert b'<form' in resp.data


def test_post_calculation(client):
    data = {
        'ek_netto': '100',
        'mwst': '19',
        'aufschlag': '10',
        'aufschlag_typ': '%'
    }
    resp = client.post('/', data=data)
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '130.90 €' in html
