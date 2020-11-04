# Generated by Django 3.1.2 on 2020-10-15 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imicusfat", "0011_auto_20201004_0936"),
    ]

    operations = [
        migrations.CreateModel(
            name="AaImicusFAT",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Alliance Auth ImicusFAT",
                "permissions": (
                    ("basic_access", "Can access the Alliance Auth ImicusFAT module"),
                ),
                "managed": False,
                "default_permissions": (),
            },
        ),
    ]