# Generated by Django 2.2.5 on 2020-12-01 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0004_auto_20201126_1631"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historico",
            name="contexto_violencia",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="historico",
            name="contexto_violencia_de_genero",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="historico",
            name="fecha",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="historico",
            name="lugar",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
