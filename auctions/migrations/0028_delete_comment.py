# Generated by Django 4.2.7 on 2023-11-24 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_remove_comment_listing'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
