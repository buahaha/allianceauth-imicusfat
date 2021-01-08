# Generated by Django 3.1.4 on 2020-12-24 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imicusfat", "0002_auto_20201020_1159"),
    ]

    operations = [
        migrations.AddField(
            model_name="ifatlink",
            name="esi_fleet_id",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="ifatlink",
            name="is_registered_on_esi",
            field=models.BooleanField(
                default=False,
                help_text="Whether this is an ESI fat link is registered on ESI",
            ),
        ),
    ]
