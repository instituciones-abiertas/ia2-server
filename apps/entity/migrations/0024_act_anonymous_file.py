from django.db import migrations
import private_storage.fields
import private_storage.storage.files
import apps.entity.validator
import os
from ..models import Act


def set_anonymus_file(apps, schema_editor):
    entity_db = schema_editor.connection.alias
    # Get the model
    ActSample = apps.get_model("entity", "Act")

    # Loop through all objects and set act.anonymous_file
    for act in ActSample.objects.using(entity_db).all():
        act.anonymous_file = act.file
        act.file = ""
        act.save()


class Migration(migrations.Migration):

    dependencies = [
        ("entity", "0023_act_hashtext"),
    ]

    operations = [
        migrations.AddField(
            model_name="act",
            name="anonymous_file",
            field=private_storage.fields.PrivateFileField(
                blank=True,
                max_length=2000,
                null=True,
                storage=private_storage.storage.files.PrivateFileSystemStorage(),
                upload_to="",
            ),
        ),
        migrations.AlterField(
            model_name="act",
            name="file",
            field=private_storage.fields.PrivateFileField(
                max_length=200,
                storage=private_storage.storage.files.PrivateFileSystemStorage(),
                upload_to="",
                validators=[apps.entity.validator.get_file_extension, apps.entity.validator.name_length],
                blank=True,
                null=True,
            ),
        ),
        migrations.RunPython(set_anonymus_file, atomic=True),
    ]
