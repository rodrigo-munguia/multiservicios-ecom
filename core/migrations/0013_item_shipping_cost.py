# Generated by Django 4.1.5 on 2023-02-08 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_order_reminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='shipping_cost',
            field=models.FloatField(default=0),
        ),
    ]
