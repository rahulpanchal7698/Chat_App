# Generated by Django 4.2.4 on 2023-08-11 12:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_friendrequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="friendrequest",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
