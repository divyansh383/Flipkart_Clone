# Generated by Django 4.0.1 on 2022-09-09 06:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_alter_tracker_tracking_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracker',
            name='deliveredtime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tracker',
            name='dispatchedtime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tracker',
            name='ofdtime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tracker',
            name='receivedtime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tracker',
            name='ofdmsg',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='receivedmsg',
            field=models.TextField(default='', null=True),
        ),
    ]
