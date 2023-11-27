# Generated by Django 4.2.7 on 2023-11-24 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0029_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='listing',
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listingComment', to='auctions.listing'),
        ),
    ]
