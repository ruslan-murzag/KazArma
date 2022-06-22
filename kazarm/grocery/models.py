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
    first_m = models.IntegerField(default=0)
    second_m = models.IntegerField(default=0)

    @property
    def calc(self):
        return self.first_m - self.second_m


    def __str__(self):
        return self.numbers_auto


class Warehouse(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Container(models.Model):


    STATUS_CHOICES = (
        ('Склад', 'Склад'),
        ('Продажа', 'Продажа'),
        ('Отходы', 'Отходы')
    )
    title = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='container')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='container')
    mass1 = models.IntegerField(default=0)
    mass2 = models.IntegerField(default=0)
    box_mass = models.IntegerField(default=0)



    def calc_netto(self):
        box_mass1 = 100
        return self.mass1 - box_mass1

    def calc_mass(self):
        m = self.mass2 - self.box_mass
        different = m - self.calc_netto()
        return different

    def __str__(self):
        return str(self.id)
