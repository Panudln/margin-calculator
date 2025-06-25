import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app
from decimal import Decimal, ROUND_HALF_UP, getcontext

getcontext().rounding = ROUND_HALF_UP

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def q2(d: Decimal) -> Decimal:
    return d.quantize(Decimal('0.01'))

def test_multi_items(client):
    data = {
        'desc[]': ['A', 'B'],
        'qty[]': ['2', '1'],
        'price[]': ['3', '5'],
        'mwst': '19',
        'aufschlag': '10',
        'aufschlag_typ': '%'
    }
    resp = client.post('/multi', data=data)
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    ek1 = q2(Decimal('2') * Decimal('3'))
    vk1 = q2(ek1 * Decimal('1.1'))
    margin1 = q2(vk1 - ek1)
    ek2 = q2(Decimal('1') * Decimal('5'))
    vk2 = q2(ek2 * Decimal('1.1'))
    margin2 = q2(vk2 - ek2)
    total_margin = q2(margin1 + margin2)
    assert 'A' in html and 'B' in html
    assert f"{total_margin:.2f} €" in html
