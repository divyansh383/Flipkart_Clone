# Generated by Django 4.0.1 on 2022-09-16 18:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_product_avgrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='added',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
