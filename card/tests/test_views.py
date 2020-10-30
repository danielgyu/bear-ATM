import pytest, json, bcrypt

from card.models import(
    Bin,
    Card
)

from card.views import (
    Validate,
    Balance,
    Deposit,
    Withdraw
)

@pytest.fixture
def sample_card(db):
    salt = bcrypt.gensalt()
    pin = str.encode('1234')
    hashed_pin = bcrypt.hashpw(pin, salt).decode('utf-8')
    card = Card.objects.create(
        number = '0123456',
        pin = hashed_pin,
        balance = 1000,
    )
    cash_bin = Bin.objects.create(
        balance = 10000
    )
    return card, cash_bin

def test_validate_success(client, sample_card):
    body = {"card_id": 1, "pin": "1234"}

    response = client.post(
        '/card/validate',
        json.dumps(body),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.json() == {'msg' : 'VALIDATION SUCCESS'}

def test_validate_fail(client, sample_card):
    body = {"card_id": 1, "pin": "987"}

    response = client.post(
        '/card/validate',
        json.dumps(body),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.json() == {'msg': 'WRONG PIN'}

def test_balance(client, sample_card):
    card, cash_bin = sample_card
    balance = card.balance

    response = client.get(
        '/card/balance/1',
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.json() == {'balance': balance}

def test_deposit(client, sample_card):
    card, cash_bin = sample_card
    body = {'deposit': 100, 'card_id': 1, 'bin_id': 1}

    response = client.post(
        '/card/deposit',
        json.dumps(body),
        content_type='application/json'
    )
    balance = card.balance + 100
    assert response.status_code == 200
    assert response.json() == {'deposit': balance}

def test_withdraw(client, sample_card):
    body =  {'withdraw': 100, 'card_id': 1, 'bin_id': 1}

    response = client.post(
        '/card/withdraw',
        json.dumps(body),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.json() == {'withdrawal': 900}

def test_withdraw_card_fail(client, sample_card):
    body =  {'withdraw': 5000, 'card_id': 1, 'bin_id': 1}

    response = client.post(
        '/card/withdraw',
        json.dumps(body),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.json() == {'error': 'not enough balance in card'}

def test_withdraw_bin_fail(client, sample_card):
    body =  {'withdraw': 20000, 'card_id': 1, 'bin_id': 1}

    response = client.post(
        '/card/withdraw',
        json.dumps(body),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.json() == {'error': 'not enough balance in bin'}
