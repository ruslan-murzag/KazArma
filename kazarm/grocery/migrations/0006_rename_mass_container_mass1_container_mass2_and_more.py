# Generated by Django 4.0.5 on 2022-06-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0005_warehouse_container'),
    ]

    operations = [
        migrations.RenameField(
            model_name='container',
            old_name='mass',
            new_name='mass1',
        ),
        migrations.AddField(
            model_name='container',
            name='mass2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='container',
            name='mass_product',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='container',
            name='status',
            field=models.CharField(choices=[('Склад', 'Склад'), ('Продажа', 'Продажа'), ('Отходы', 'Отходы')], default='', max_length=10),
        ),
    ]
