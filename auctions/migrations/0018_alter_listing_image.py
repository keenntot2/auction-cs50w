# Generated by Django 4.2.7 on 2023-11-22 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.CharField(default='igiiiit', max_length=5000),
        ),
    ]
