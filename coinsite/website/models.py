from django.db import models


class Coin(models.Model):

    currency = models.CharField(max_length=255)
    price = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()
    korean = models.CharField(max_length=255)


