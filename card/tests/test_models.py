import pytest
import bcrypt

from card.models import (
    Bin,
    Card
)

@pytest.mark.django_db
def test_create_card():
    salt = bcrypt.gensalt()
    hashed_pin = bcrypt.hashpw(str.encode('123'), salt)
    card = Card.objects.create(
        number = '0123456789',
        pin = hashed_pin,
    )
    assert card.id == 1
    assert card.number == '0123456789'
    assert card.pin == hashed_pin
    assert card.balance == 0

@pytest.mark.django_db
def test_create_bin():
    cash_bin = Bin.objects.create(
        balance = 10000
    )
    assert cash_bin.id == 1
    assert cash_bin.balance == 10000

