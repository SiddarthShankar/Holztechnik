# Generated by Django 4.2.16 on 2024-12-06 17:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0015_remove_picking_order_spec_remove_picking_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="picking",
            name="article_id",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ]
            ),
        ),
    ]