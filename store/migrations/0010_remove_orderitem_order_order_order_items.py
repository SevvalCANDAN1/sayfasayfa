# Generated by Django 5.1.3 on 2025-01-18 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_order_total_price_order_total_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='order_items',
            field=models.ManyToManyField(related_name='order_items', to='store.orderitem'),
        ),
    ]
