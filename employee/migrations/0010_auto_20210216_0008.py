# Generated by Django 3.0.8 on 2021-02-16 00:08

from django.db import migrations, models
import storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_employee_completed_orientation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='birth_certificate',
            field=models.FileField(blank=True, null=True, storage=storage_backends.PrivateMediaStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='i9',
            field=models.FileField(blank=True, null=True, storage=storage_backends.PrivateMediaStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='social_security_card',
            field=models.FileField(blank=True, null=True, storage=storage_backends.PrivateMediaStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='vaccination_record',
            field=models.FileField(blank=True, null=True, storage=storage_backends.PrivateMediaStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='w4',
            field=models.FileField(blank=True, null=True, storage=storage_backends.PrivateMediaStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='workers_comp',
            field=models.FileField(blank=True, null=True, storage=storage_backends.PrivateMediaStorage(), upload_to=''),
        ),
    ]
