# Generated by Django 4.1.2 on 2022-10-23 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0002_vendor_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendor",
            name="active",
            field=models.BooleanField(default=False),
        ),
    ]
