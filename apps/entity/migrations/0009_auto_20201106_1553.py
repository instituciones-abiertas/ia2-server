# Generated by Django 2.2.5 on 2020-11-06 18:53

from django.db import migrations
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ("entity", "0008_auto_20201105_1845"),
    ]

    operations = [
        migrations.AlterField(
            model_name="act",
            name="file",
            field=private_storage.fields.PrivateFileField(
                max_length=200, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=""
            ),
        ),
    ]
