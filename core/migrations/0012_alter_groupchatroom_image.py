# Generated by Django 4.2.4 on 2023-08-14 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_alter_groupchatroom_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupchatroom",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="group_image"),
        ),
    ]
