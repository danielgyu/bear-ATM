import pytest
import bcrypt

from card.errors import ShortageError

from card.models import (
    Bin,
    Card
)

from card.service import (
    get_card_info,
    get_card_balance,
    deposit_card,
    withdraw_card,
    check_pin
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
    return card

def test_get_card_info(sample_card):
    card = get_card_info(1)
    assert card.id == sample_card.id
    assert card.number == sample_card.number
    assert card.balance == sample_card.balance

def test_check_pin(sample_card):
    entered_pin = '1234'
    res = check_pin(1, entered_pin)
    assert res == True

def test_get_card_balance(sample_card):
    res, _ = get_card_balance(1)
    assert res == sample_card.balance

def test_deposit_card(sample_card):
    res = deposit_card(1, 100)
    assert res.balance == 1100

def test_withdraw_card(sample_card):
    res = withdraw_card(1, 100)
    assert res.balance == 900

def test_withdraw_card_fail(sample_card):
    with pytest.raises(ShortageError, match = 'not enough balance in card'):
        withdraw_card(1, 10000)

