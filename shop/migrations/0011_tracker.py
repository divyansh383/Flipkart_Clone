# Generated by Django 4.0.1 on 2022-09-09 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_orders_dispatched'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isdispatched', models.BooleanField(default=False)),
                ('isreceived', models.BooleanField(default=False)),
                ('receivedmsg', models.TextField(default='')),
                ('isofd', models.BooleanField(default=False)),
                ('ofdmsg', models.TextField(default='')),
                ('isdelivered', models.BooleanField(default=False)),
                ('tracking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.orders')),
            ],
        ),
    ]
