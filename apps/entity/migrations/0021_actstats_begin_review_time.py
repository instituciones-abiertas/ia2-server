# Generated by Django 2.2.5 on 2021-05-11 18:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("entity", "0020_actstats_review_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="actstats",
            name="begin_review_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
