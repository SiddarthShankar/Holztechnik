# Generated by Django 4.2.16 on 2024-10-22 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0008_order_pdf_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="Picking",
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
                ("quantity", models.PositiveIntegerField(default=1)),
                ("item_to_pick", models.CharField(max_length=255)),
                (
                    "order_spec",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="website.orderspecs",
                    ),
                ),
            ],
        ),
    ]
