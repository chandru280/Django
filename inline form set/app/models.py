from datetime import timezone
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class ProductMeta(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField('Property', max_length=50)
    value = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'Id: {self.pk }, {self.name} for ProductId: {self.product.pk}'
    




