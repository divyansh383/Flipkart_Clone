# Generated by Django 4.0.1 on 2022-09-05 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_orders_quantity_alter_orders_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
    ]
