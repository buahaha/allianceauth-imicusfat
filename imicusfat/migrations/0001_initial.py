# Generated by Django 2.0.6 on 2018-06-06 07:57

import imicusfat.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eveonline', '0010_alliance_ticker'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IFat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system', models.CharField(max_length=30)),
                ('shiptype', models.CharField(max_length=30)),
                ('station', models.CharField(max_length=125)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eveonline.EveCharacter')),
            ],
        ),
        migrations.CreateModel(
            name='IFatLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ifattime', models.DateTimeField(default=django.utils.timezone.now)),
                ('fleet', models.CharField(max_length=254)),
                ('hash', models.CharField(max_length=254)),
                ('creator', models.ForeignKey(on_delete=models.SET(imicusfat.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ifat',
            name='ifatlink',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imicusfat.IFatLink'),
        ),
        migrations.AddField(
            model_name='ifat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='ifat',
            unique_together={('character', 'ifatlink')},
        ),
    ]
