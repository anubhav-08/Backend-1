# Generated by Django 3.1.4 on 2021-10-11 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210112_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_bot',
            field=models.BooleanField(default=False),
        ),
    ]