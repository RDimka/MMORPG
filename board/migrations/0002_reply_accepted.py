# Generated by Django 4.1.5 on 2023-03-18 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
