from django.db import models


class Coin(models.Model):

    name = models.CharField()
    price = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    volume = models.IntegerField()
    volume_price = models.IntegerField()

    class Meta:
        ordering = ['-volume_price']

