# Generated by Django 2.0.7 on 2019-11-19 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20191119_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='producer',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
