# Generated by Django 4.0.1 on 2022-08-28 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_remove_orders_updated_on_orders_qty_alter_orders_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]