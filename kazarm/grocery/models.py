from django.db import models


class Store(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Клиенты'
        verbose_name_plural = 'Клиенты'


class Product(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'


class First_stage(models.Model):
    title = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    numbers_auto = models.CharField(max_length=15)
    first_m = models.FloatField(default=0)
    second_m = models.FloatField(default=0)

    @property
    def calc(self):
        return self.first_m - self.second_m


    def __str__(self):
        return self.numbers_auto

    class Meta:
        verbose_name = 'Приход'
        verbose_name_plural = 'Приход'


class Warehouse(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def warehouse_len(self):
        # return 'Hello world'
        return len(self.container.all().filter(status='Склад'))

    def warehouse_sell_len(self):
        return len(self.container.all().filter(status='Продажа'))

    def container_mass(self):
        containers_warehouse = self.container.all().filter(status='Склад')
        containers_sales = self.container.all().filter(status='Продажа')
        massa_warehouse = 0
        massa_sales = 0

        for i in containers_warehouse:
            massa_warehouse += i.calc_netto1()
        for i in containers_sales:
            massa_sales += i.calc_netto1()

        return [massa_warehouse, massa_sales]
    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склад'


class Container(models.Model):
    STATUS_CHOICES = (
        ('Склад', 'Склад'),
        ('Сортировка', 'Сортировка'),
        ('Продажа', 'Продажа'),
        ('Отходы', 'Отходы'),
        ('Отгружено', 'Отгружено')
    )
    title = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='container')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='')
    status1 = models.CharField(max_length=10, choices=STATUS_CHOICES, default='', blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='container')
    mass1 = models.FloatField(default=0)
    mass2 = models.FloatField(default=0)
    box_mass1 = models.FloatField(default=0)
    box_mass2 = models.FloatField(default=0)
    stores = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='containers', blank=True, null=True)

    class Meta:
        verbose_name = 'Контейнер'
        verbose_name_plural = 'Контейнер'

    def calc_netto1(self):
        return round(self.mass1 - self.box_mass1, 3)

    def calc_netto2(self):
        return round(self.mass2 - self.box_mass2, 3)

    def calc_mass(self):
        different = self.calc_netto2() - self.calc_netto1()
        return round(different, 3)

    def __str__(self):
        return str(self.id)


