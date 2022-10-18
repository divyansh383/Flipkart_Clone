# Generated by Django 4.0.1 on 2022-09-14 09:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0014_product_rating_seller_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='rating',
            new_name='avgrating',
        ),
        migrations.AlterField(
            model_name='seller',
            name='contact',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)]),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('review', models.TextField(default='', null=True)),
                ('reviewer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reviewitem', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
    ]
