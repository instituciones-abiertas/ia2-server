from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("entity", "0024_act_anonymous_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="ocurrencyentity",
            name="ner_index",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

