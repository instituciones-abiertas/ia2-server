# Generated by Django 2.2.5 on 2021-05-26 22:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("entity", "0021_actstats_begin_review_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="actstats",
            name="find_all_ocurrencies",
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
