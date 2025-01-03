# Generated by Django 5.1.2 on 2024-11-29 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_category_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.customerprofile')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.product')),
            ],
        ),
    ]
