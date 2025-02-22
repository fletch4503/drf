# Generated by Django 5.1.1 on 2024-09-15 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(db_index=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="ewsitem",
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
                ("email_title", models.CharField(max_length=250)),
                ("sender", models.EmailField(max_length=254)),
                ("time_receive", models.DateTimeField(auto_now_add=True)),
                ("done", models.BooleanField(default=False)),
                (
                    "cat",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="ews_list.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "EWS Item",
                "ordering": ("id",),
            },
        ),
    ]
