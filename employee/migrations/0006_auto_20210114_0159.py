# Generated by Django 3.0.8 on 2021-01-14 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_remove_transportation_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='account_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='account_type',
            field=models.CharField(blank=True, choices=[('S', 'Savings Account'), ('C', 'Checkings Account')], default=None, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='auth_signature',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='awknowledgement_form_signature',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='banking_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='email_address',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='i9',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='photo_id',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='savings_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='social_security_card',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='social_security_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='w4',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='workers_comp',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='employee',
            name='is_hired',
            field=models.BooleanField(blank=True, choices=[(True, 'Yes'), (False, 'No')], null=True, verbose_name='hire'),
        ),
    ]
