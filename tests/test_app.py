import os
import sys
import pytest

# Ensure the app module is importable when tests are run from any directory
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

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


def test_negative_ek_netto(client):
    data = {
        'ek_netto': '-1',
        'mwst': '19',
    }
    resp = client.post('/', data=data)
    html = resp.data.decode()
    assert 'EK Netto darf nicht negativ sein.' in html


def test_vat_over_hundred(client):
    data = {
        'ek_netto': '100',
        'mwst': '120',
    }
    resp = client.post('/', data=data)
    html = resp.data.decode()
    assert 'MwSt muss zwischen 0 und 100 liegen.' in html


def test_negative_markup(client):
    data = {
        'ek_netto': '100',
        'mwst': '19',
        'aufschlag': '-5',
        'aufschlag_typ': '%'
    }
    resp = client.post('/', data=data)
    html = resp.data.decode()
    assert 'Aufschlag darf nicht negativ sein.' in html
