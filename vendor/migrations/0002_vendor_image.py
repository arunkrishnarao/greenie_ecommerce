# Generated by Django 3.2.4 on 2022-10-15 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='./'),
        ),
    ]
