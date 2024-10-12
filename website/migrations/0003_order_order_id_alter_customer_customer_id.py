# Generated by Django 4.2.13 on 2024-10-12 20:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0002_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_id",
            field=models.CharField(default="00000", max_length=5),
        ),
        migrations.AlterField(
            model_name="customer",
            name="customer_id",
            field=models.CharField(max_length=5),
        ),
    ]