import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db

@pytest.fixture()
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()


def test_margin_calculation(client):
    resp = client.post('/', data={
        'ek_netto': '10',
        'mwst': '19',
        'aufschlag': '10',
        'aufschlag_typ': '%'
    })
    assert resp.status_code == 200
    assert b'VK Brutto' in resp.data


def test_quote_saved_and_listed(client):
    client.post('/', data={'ek_netto': '10', 'mwst': '19'})
    resp = client.get('/quotes')
    assert b'Angebot #1' in resp.data

