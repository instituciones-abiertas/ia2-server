# Generated by Django 2.2.5 on 2020-11-25 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Historico",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha", models.CharField(max_length=200)),
                ("lugar", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Lugar",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("_nombre", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Hecho",
            fields=[
                ("contexto_violencia", models.BooleanField(default=False)),
                ("contexto_violencia_de_genero", models.BooleanField(default=False)),
                ("_fecha", models.DateField()),
                (
                    "historico",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="data.Historico",
                    ),
                ),
                ("lugares", models.ManyToManyField(to="data.Lugar")),
            ],
        ),
    ]
