import json

from django.http      import JsonResponse
from django.shortcuts import render
from django.views     import View

from .errors import ShortageError
from .models import Bin, Card
from .service import (
    get_bin_info, get_bin_balance, deposit_bin, withdraw_bin,
    get_card_info, check_pin, get_card_balance, deposit_card, withdraw_card
)

class Validate(View):
    def post(self, request):
        payload = json.loads(request.body)
        card_id = payload['card_id']
        pin     = payload['pin']

        if check_pin(card_id, pin):
            return JsonResponse({'msg' : 'VALIDATION SUCCESS'}, status = 200)
        else:
            return JsonResponse({'msg' : 'WRONG PIN'}, status =  400)

class Balance(View):
    def get(self, request, pk):
        amount, _ = get_card_balance(pk)
        return JsonResponse({'balance' : amount}, status = 200)

class Deposit(View):
    def post(self, request):
        payload = json.loads(request.body)
        amount  = payload['deposit']
        card_id = payload['card_id']
        bin_id  = payload['bin_id']

        card = deposit_card(card_id, amount)
        cash_bin = deposit_bin(bin_id, amount)

        return JsonResponse({'deposit' : card.balance}, status = 200)

class Withdraw(View):
    def post(self, request):
        payload = json.loads(request.body)
        amount  = payload['withdraw']
        card_id = payload['card_id']
        bin_id  = payload['bin_id']

        try:
            cash_bin = withdraw_bin(bin_id, amount)
            card = withdraw_card(card_id, amount)
        except ShortageError as e:
            return JsonResponse({'error' : e.msg}, status = 400)
        else:
            return JsonResponse({'withdrawal' : card.balance}, status = 200)
