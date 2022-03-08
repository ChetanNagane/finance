from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    cash = models.FloatField(max_length=20, default=10000)


# class Stock(models.Model):
#     symbol = models.CharField(max_length=64)
#     price = models.FloatField(max_length=20)


class Stocks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    symbol = models.CharField(max_length=64)
    price = models.FloatField(max_length=20)
    LTP = 1

    @property
    def current(self):
        from .views import getPrice
        return round(self.LTP*self.quantity, 2)
        return round(getPrice(self.symbol)["price"]*self.quantity, 2)

    @property
    def invested(self):
        return round(self.price*self.quantity, 2)

    @property
    def currentPrice(self):
        from .views import getPrice
        return self.LTP
        return round(getPrice(self.symbol)["price"], 2)

    @property
    def profitLoss(self):
        return round(self.current - self.invested, 2)

    def __str__(self) -> str:
        return f"{self.user} has {self.quantity} shares of {self.symbol} with avg price {self.price}"


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    symbol = models.CharField(max_length=64)
    price = models.FloatField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
