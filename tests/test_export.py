import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import app

@pytest.fixture

def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def calculate(client):
    return client.post('/', data={
        'ek_netto': '100',
        'mwst': '19',
        'aufschlag': '20',
        'aufschlag_typ': '%'
    })

def test_csv_export(client):
    calculate(client)
    resp = client.get('/export?format=csv')
    assert resp.status_code == 200
    assert resp.headers['Content-Type'] == 'text/csv'
    assert b'EK Netto' in resp.data

def test_pdf_export(client):
    calculate(client)
    resp = client.get('/export?format=pdf')
    assert resp.status_code == 200
    assert resp.headers['Content-Type'] == 'application/pdf'
    assert resp.data.startswith(b'%PDF')
