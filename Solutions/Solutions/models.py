from django.db import models


class Item(models.Model):
    name = models.CharField('Product Name', max_length=40)
    description = models.CharField('Product Description', max_length=200)
    price = models.DecimalField("Product price", max_digits=8, decimal_places=2)
    # currency = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    user = models.CharField("user_cookies", max_length=30)
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
