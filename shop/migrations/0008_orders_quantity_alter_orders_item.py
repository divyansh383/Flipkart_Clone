# Generated by Django 4.0.1 on 2022-08-31 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_remove_orders_qty_alter_orders_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='orders',
            name='item',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
        ),
    ]
