# Generated by Django 3.1.1 on 2020-09-27 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imicusfat", "0009_ifatlink_is_esilink"),
    ]

    operations = [
        migrations.AddField(
            model_name="ifatlinktype",
            name="is_enabled",
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
