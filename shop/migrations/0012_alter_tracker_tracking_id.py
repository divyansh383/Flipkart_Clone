# Generated by Django 4.0.1 on 2022-09-09 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_tracker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='tracking_id',
            field=models.TextField(default=''),
        ),
    ]
