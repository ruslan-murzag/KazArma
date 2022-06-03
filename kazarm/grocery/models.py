from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class First_stage(models.Model):
    title = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    numbers_auto = models.CharField(max_length=15)
    first_m = models.IntegerField(blank=True, null=True)
    second_m = models.IntegerField(blank=True, null=True)

    # product_m = models.IntegerField(blank=True)

    @property
    def calc(self):
        if self.second_m is not None and self.first_m is not None:
            return self.first_m - self.second_m
        return

    def __str__(self):
        return self.numbers_auto
