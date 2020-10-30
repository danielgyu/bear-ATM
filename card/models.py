from django.db import models

class Card(models.Model):
    number  = models.CharField(max_length=32)
    pin     = models.CharField(max_length = 200)
    balance = models.PositiveBigIntegerField(default = 0)

class Bin(models.Model):
    balance = models.PositiveBigIntegerField(default = 0)
