# Generated by Django 2.2.5 on 2020-11-26 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("entity", "0011_ocurrencyentity_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ocurrencyentity",
            name="text",
            field=models.TextField(blank=True, null=True),
        ),
    ]
