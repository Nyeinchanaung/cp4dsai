from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200, blank=True, null=True )
    class Meta:
        verbose_name_plural = "Categories"

class Result(models.Model):
    categories = models.ManyToManyField(Category)
    age = models.PositiveIntegerField(default=0, blank=True, null=True)
    payment_method = models.CharField(max_length=200, default=None, blank=True, null=True)
    state = models.CharField(max_length=200, default=None, blank=True, null=True)
    discount_percent = models.DecimalField(max_digits=4, decimal_places=2, default=0, blank=True, null=True)
    customer_type = models.CharField(max_length=200, default=None, blank=True, null=True)
