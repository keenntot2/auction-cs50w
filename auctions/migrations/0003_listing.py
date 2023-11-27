# Generated by Django 4.2.7 on 2023-11-21 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=5000)),
                ('startingBid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.CharField(max_length=5000)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.category')),
            ],
        ),
    ]
