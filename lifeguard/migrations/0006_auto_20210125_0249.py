# Generated by Django 3.0.8 on 2021-01-25 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifeguard', '0005_auto_20210120_0251'),
    ]

    operations = [
        migrations.AddField(
            model_name='lifeguardclass',
            name='is_refresher',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Is this class a refresher?'),
        ),
        migrations.AddField(
            model_name='lifeguardclass',
            name='refresher_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lifeguardclass',
            name='is_review',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Is this class a review?'),
        ),
    ]
