# Generated by Django 4.1.2 on 2023-03-03 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_settings_delete_frontpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='email',
            field=models.CharField(default='', max_length=500),
        ),
    ]
