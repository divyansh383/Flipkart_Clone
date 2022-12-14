# Generated by Django 4.0.1 on 2022-08-28 08:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_orders_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='order_id',
        ),
        migrations.AddField(
            model_name='orders',
            name='id',
            field=models.BigAutoField(auto_created=True, default=django.utils.timezone.now, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='order_code',
            field=models.CharField(default='', max_length=500),
        ),
    ]
