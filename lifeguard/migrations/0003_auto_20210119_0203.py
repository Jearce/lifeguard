# Generated by Django 3.0.8 on 2021-01-19 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifeguard', '0002_lifeguardclasssession'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lifeguardclass',
            options={'verbose_name': 'Session'},
        ),
        migrations.AlterModelOptions(
            name='lifeguardclasssession',
            options={'verbose_name': 'Session date'},
        ),
        migrations.AlterField(
            model_name='lifeguardclass',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='lifeguardclass',
            name='start_date',
            field=models.DateField(),
        ),
    ]
