# Generated by Django 4.2.13 on 2024-10-12 20:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0003_order_order_id_alter_customer_customer_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="is_deleted",
        ),
    ]