# Generated by Django 4.2.7 on 2023-11-29 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_order_address_order_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Cart',
            new_name='cart',
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
