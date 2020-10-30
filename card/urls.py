from django.urls import path

from .views import Validate, Balance, Deposit, Withdraw

urlpatterns= [
    path('/validate', Validate.as_view()),
    path('/balance/<int:pk>', Balance.as_view()),
    path('/deposit', Deposit.as_view()),
    path('/withdraw', Withdraw.as_view()),
]
