# Generated by Django 3.0.8 on 2021-01-20 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifeguard', '0004_lifeguard_online_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='enroll',
            name='brick',
            field=models.BooleanField(blank=True, null=True, verbose_name='Passed brick test'),
        ),
        migrations.AddField(
            model_name='enroll',
            name='swim_300',
            field=models.BooleanField(blank=True, null=True, verbose_name='Can swim 300 meters'),
        ),
        migrations.AddField(
            model_name='enroll',
            name='tread',
            field=models.BooleanField(blank=True, null=True, verbose_name='Can tread for 2 minutes'),
        ),
    ]
