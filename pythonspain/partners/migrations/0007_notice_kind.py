# Generated by Django 3.1.7 on 2021-02-28 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0006_auto_20200627_1526"),
    ]

    operations = [
        migrations.AddField(
            model_name="notice",
            name="kind",
            field=models.CharField(
                choices=[("late", "Late"), ("annual", "Annual")],
                default="late",
                max_length=16,
                verbose_name="kind",
            ),
        ),
    ]
