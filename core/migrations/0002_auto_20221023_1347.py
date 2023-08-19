# Generated by Django 3.2.4 on 2022-10-23 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontpage',
            name='facebook',
            field=models.CharField(default='https://www.facebook.com/', max_length=500),
        ),
        migrations.AddField(
            model_name='frontpage',
            name='instagram',
            field=models.CharField(default='https://www.instagram.com/', max_length=500),
        ),
        migrations.AddField(
            model_name='frontpage',
            name='twitter',
            field=models.CharField(default='https://www.twitter.com/', max_length=500),
        ),
        migrations.AlterField(
            model_name='frontpage',
            name='heading',
            field=models.CharField(max_length=200),
        ),
    ]
