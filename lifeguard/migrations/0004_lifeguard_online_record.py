# Generated by Django 3.0.8 on 2021-01-19 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifeguard', '0003_auto_20210119_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='lifeguard',
            name='online_record',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]