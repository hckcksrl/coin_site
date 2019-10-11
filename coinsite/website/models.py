from django.db import models


class Coin(models.Model):

    currency = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    high = models.FloatField(default=0)
    low = models.FloatField(default=0)
    volume = models.FloatField(default=0)
    korean = models.CharField(max_length=255,default=True)
    rate = models.FloatField(default=0)


