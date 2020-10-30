import bcrypt

from .errors import ShortageError
from .models import (
    Bin,
    Card
)


"""api for cash_bin"""
def get_bin_info(obj_id):
    obj = Bin.objects.get(id = obj_id)
    return obj

def get_bin_balance(obj_id):
    obj = get_bin_info(obj_id)
    return obj.balance, obj

def deposit_bin(obj_id, amount):
    balance, obj = get_bin_balance(obj_id)
    balance += amount
    obj.balance = balance
    obj.save()

def withdraw_bin(obj_id, amount):
    balance, obj = get_bin_balance(obj_id)

    if balance > amount:
        obj.balance - amount
        obj.save()
    else:
        raise ShortageError('not enough balance in bin')
    return obj

"""api for bank-card"""

def get_card_info(obj_id):
    obj = Card.objects.get(id = obj_id)
    return obj

def check_pin(card_id, entered_pin):
    card        = get_card_info(card_id)
    entered_pin = str.encode(entered_pin)
    card_pin    = str.encode(card.pin)

    if bcrypt.checkpw(entered_pin, card_pin):
        return True
    else:
        return False

def get_card_balance(obj_id):
    obj = get_card_info(obj_id)
    return obj.balance, obj

def deposit_card(obj_id, amount):
    balance, obj = get_card_balance(obj_id)
    balance += amount
    obj.balance = balance
    obj.save()
    return obj

def withdraw_card(obj_id, amount):
    balance, obj = get_card_balance(obj_id)

    if balance > amount:
        obj.balance -= amount
        obj.save()
    else:
        raise ShortageError('not enough balance in card')
    return obj
