# Generated by Django 2.2.5 on 2020-12-22 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0005_auto_20201201_1438"),
    ]

    operations = [
        migrations.AddField(
            model_name="hecho",
            name="_edad_acusadx",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="hecho",
            name="_edad_victima",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historico",
            name="edad_acusadx",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historico",
            name="edad_victima",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
