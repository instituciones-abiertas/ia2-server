# Generated by Django 2.2.5 on 2020-09-18 18:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='act',
            name='text',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='OcurrencyEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startIndex', models.PositiveIntegerField()),
                ('endIndex', models.PositiveIntegerField()),
                ('act', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listOfEntity', to='entity.Act')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.Entity')),
            ],
        ),
    ]