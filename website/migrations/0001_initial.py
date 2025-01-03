# Generated by Django 4.2.13 on 2024-10-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("customer_id", models.IntegerField(max_length=10)),
                ("name", models.CharField(max_length=20)),
                ("email", models.CharField(max_length=30)),
                ("phone", models.CharField(max_length=15)),
                ("address", models.CharField(max_length=100)),
            ],
        ),
    ]
