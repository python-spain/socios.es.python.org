# Generated by Django 3.0.4 on 2020-06-27 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0005_auto_20200402_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='number',
            field=models.CharField(blank=True, db_index=True, max_length=10, unique=True, verbose_name='number'),
        ),
    ]
